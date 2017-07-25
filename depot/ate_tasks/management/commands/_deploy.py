# coding=utf-8
"""

基于zerorpc和OpenStack的taskflow开发的测试引擎组件，具备远程调用功能。
详情参考 https://docs.openstack.org/developer/taskflow/index.html

"""
import abc
import functools
import json
import logging
import threading
import uuid

import zerorpc
from channels import Group
from channels.management.commands.runserver import Command as RunserverCommand
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import ObjectDoesNotExist
from gevent.pool import Pool
from gevent.queue import Queue
from taskflow import engines, task
from taskflow.patterns import linear_flow
from taskflow.types import notifier

from ate_tasks.models import TaskInstance

if settings.TEST_ENGINE_SETTINGS:
    TEST_ENGINE_SETTINGS = settings.TEST_ENGINE_SETTINGS
else:
    TEST_ENGINE_SETTINGS = {}
ENGINE_ADDRESS = TEST_ENGINE_SETTINGS.get('ADDRESS', 'tcp://localhost:8001')
RPC_POOL_SIZE = TEST_ENGINE_SETTINGS.get('RPC_POOL_SIZE', 100)
ENGINE_POOL_SIZE = TEST_ENGINE_SETTINGS.get('ENGINE_POOL_SIZE', 10)

LOGGER = logging.getLogger('ate.test_engine')


class BaseTask(task.Task):
    @staticmethod
    def wrap_test_record(_pass, detail, name):
        return {'pass': _pass, 'detail': detail, 'name': name}

    @staticmethod
    def validate_record(func):
        @functools.wraps(func)
        def wrapper(self, flow_id, *args):
            expected_keys = {'pass', 'detail', 'name'}
            default_record = self.wrap_test_record(False, '测试记录无效', self.name)
            record = func(self, flow_id, *args)
            if not isinstance(record, dict) or not expected_keys.issubset(record):
                record = default_record
                LOGGER.warning("任务{flow_id}测试记录无效。".format(flow_id=flow_id))
            return record

        return wrapper

    @staticmethod
    def append_record(func):
        @functools.wraps(func)
        def wrapper(self, flow_id, *args):
            record = func(self, flow_id, *args)
            try:
                task_instance = TaskInstance.objects.get(uuid=flow_id)
                task_instance.append_test_record(record)
                LOGGER.info("任务{flow_id}添加测试记录成功，记录为{record}。".format(flow_id=flow_id, record=record))
            except ObjectDoesNotExist:
                LOGGER.warning("任务{flow_id}不存在".format(flow_id=flow_id))
            return record

        return wrapper

    @abc.abstractmethod
    def execute(self, *args, **kwargs):
        pass


class TaskStart(BaseTask):
    @BaseTask.append_record
    @BaseTask.validate_record
    def execute(self, flow_id):
        record = self.wrap_test_record(True, '初始化成功', self.name)
        return record


class TaskEnd(BaseTask):
    @BaseTask.append_record
    @BaseTask.validate_record
    def execute(self, flow_id):
        record = self.wrap_test_record(True, '结束成功', self.name)
        return record


class TaskCustom(BaseTask):
    def __init__(self, code, parameters, publish_message, publish_window, get_window_result, **kwargs):
        self.code = code
        self.parameters = parameters
        self.publish_message = publish_message
        self.publish_window = publish_window
        self.get_window_result = get_window_result
        super(TaskCustom, self).__init__(**kwargs)

    @BaseTask.append_record
    @BaseTask.validate_record
    def execute(self, flow_id):
        try:
            code = compile(self.code, self.name, 'exec')
            ns = {}
            exec(code, ns)
            ns['publish_message'] = self.publish_message
            ns['publish_window'] = self.publish_window
            record, _temp = ns['execute'](flow_id, self.parameters)
            record['name'] = self.name
        except:
            LOGGER.exception("任务{flow_id}测试项{name}异常".format(flow_id=flow_id, name=self.name))
            record = self.wrap_test_record(False, '测试项运行异常', self.name)
        return record


class TestEngine(object):
    def __init__(self, pool):
        self.pool = pool
        self.window_results = {}

    def execute(self, flow_id, flow_name, code_and_para):
        try:
            self.pool.apply_async(self.__handling, (flow_id, flow_name, code_and_para))
            return True
        except:
            LOGGER.exception("任务{flow_id}提交失败".format(flow_id=flow_id))
            return False

    def set_window_result(self, window_id, result):
        try:
            if window_id in self.window_results:
                self.window_results[window_id].put(result)
                return True
            else:
                return False
        except:
            return False

    def __handling(self, flow_id, flow_name, code_and_para):
        def group_send(content):
            Group(flow_id).send({'text': json.dumps(content, ensure_ascii=False)})

        def publish_message(message):
            content = {'message_type': 'message', 'message': message}
            group_send(content)

        def get_window_result(window_id, timeout):
            try:
                window_queue = self.window_results.get(window_id)
                if window_queue:
                    window_result = self.window_results[window_id].get(timeout=timeout)
                else:
                    window_result = None
            except:
                window_result = None
            finally:
                if window_id in self.window_results:
                    del self.window_results[window_id]
            return window_result

        def publish_window(window_detail, timeout=60):
            window_id = str(uuid.uuid1())
            self.window_results[window_id] = Queue()
            content = {'message_type': 'window', 'window_detail': window_detail, 'window_id': window_id,
                       'timeout': timeout}
            group_send(content)
            result = get_window_result(window_id, timeout)
            return result

        def flow_notification(state, details):
            content = {'message_type': 'flow_state', 'state': state}
            group_send(content)

        def task_notification(state, details):
            try:
                task_name = details['task_name']
                content = {'message_type': 'state', 'state': state, 'name': task_name}
                group_send(content)
                task_instance = TaskInstance.objects.get(uuid=flow_id)
                record = task_instance.get_record(task_name)
                if record:
                    record['message_type'] = 'result'
                    group_send(record)
            except ObjectDoesNotExist:
                LOGGER.exception('任务{flow_id}不存在'.format(flow_id=flow_id))
            except BaseException:
                LOGGER.exception('任务监视器出现异常')

        try:
            flow = linear_flow.Flow(flow_name)
            flow.add(TaskStart(name='start'))
            for item_name, item_code, item_para in code_and_para:
                flow.add(TaskCustom(item_code, item_para, name=item_name,
                                    publish_message=publish_message, publish_window=publish_window,
                                    get_window_result=get_window_result))
            flow.add(TaskEnd(name='end'))
            store = {'flow_id': flow_id}
            engine = engines.load(flow, store=store)
            engine.notifier.register(notifier.Notifier.ANY, flow_notification)
            engine.atom_notifier.register(notifier.Notifier.ANY, task_notification)
            engine.compile()
            engine.prepare()
            engine.run()
        except BaseException:
            LOGGER.exception("测试任务{flow_id}异常结束".format(flow_id=flow_id))


class Command(RunserverCommand):
    help = '启动测试执行引擎并接收测试命令'

    def handle(self, *args, **options):
        try:
            worker = EngineThread(ENGINE_POOL_SIZE, RPC_POOL_SIZE,ENGINE_ADDRESS,LOGGER)
            print(ENGINE_ADDRESS)
            worker.daemon = True
            worker.start()
            super(Command, self).handle(*args, **options)
            # pool = Pool(ENGINE_POOL_SIZE)
            # s = zerorpc.Server(TestEngine(pool=pool), pool_size=RPC_POOL_SIZE)
            # s.bind(ENGINE_ADDRESS)
            # self.stdout.write(self.style.SUCCESS('测试引擎启动：{0}'.format(ENGINE_ADDRESS)))
            # s.run()
        except BaseException as e:
            self.stdout.write(self.style.ERROR('{0}'.format(e)))
            LOGGER.exception(e)


class EngineThread(threading.Thread):
    """
    Class that runs a worker
    """

    def __init__(self, engine_pool_size,rpc_pool_size,engine_address,logger):
        super(EngineThread, self).__init__()
        self.engine_pool_size=engine_pool_size
        self.rpc_pool_size = rpc_pool_size
        self.engine_address = engine_address
        self.logger=logger

    def run(self):
        self.logger.debug("engine thread running")
        pool = Pool(self.engine_pool_size)
        s = zerorpc.Server(TestEngine(pool=pool), pool_size=self.rpc_pool_size)
        s.bind(self.engine_address)
        s.run()
        self.logger.debug("engine thread exited")
