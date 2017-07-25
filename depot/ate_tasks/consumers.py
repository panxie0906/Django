# coding=utf-8
import json

import zerorpc
from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from django.conf import settings
from django.db.models import ObjectDoesNotExist

import ate_tasks.models as models

ENGINE_ADDRESS = settings.TEST_ENGINE_SETTINGS['ADDRESS']
JSON_DUMPS_PARAMS = settings.TEST_ENGINE_SETTINGS['JSON_DUMPS_PARAMS']


@channel_session_user_from_http
def ws_add(message):
    message.reply_channel.send({"accept": True})
    group = '-'.join(message.content['path'][1:-1].split('/'))
    group_prefix = message.content['path'][1:-1].split('/')[0]
    if group_prefix == 'monitor':
        monitor_uuid = message.content['path'][1:-1].split('/')[1]
        try:
            monitor = models.Monitor.objects.get(uuid=monitor_uuid)
            monitor.is_running = True
            monitor.save()
            Group(group).add(message.reply_channel)
        except ObjectDoesNotExist:
            pass
    elif group_prefix == 'task':
        Group(group).add(message.reply_channel)


@channel_session_user
def ws_message(message):
    group_prefix = message.content['path'][1:-1].split('/')[0]
    group = '-'.join(message.content['path'][1:-1].split('/'))
    if group_prefix == 'task':
        try:
            msg_obj = json.loads(message.content['text'], encoding='utf-8')
            if msg_obj['message_type'] == 'window':
                rpc_client = zerorpc.Client()
                rpc_client.connect(ENGINE_ADDRESS)
                if not rpc_client.set_window_result(msg_obj['window_id'], msg_obj['window_result']):
                    print('设置窗体结果失败')
        except BaseException as e:
            pass
    elif group_prefix == 'monitor':
        pass


@channel_session_user
def ws_disconnect(message):
    group = '-'.join(message.content['path'][1:-1].split('/'))
    group_prefix = message.content['path'][1:-1].split('/')[0]
    if group_prefix == 'monitor':
        monitor_uuid = message.content['path'][1:-1].split('/')[1]
        try:
            monitor = models.Monitor.objects.get(uuid=monitor_uuid)
            monitor.is_running = False
            monitor.save()
            Group(group).add(message.reply_channel)
        except ObjectDoesNotExist:
            pass
    elif group_prefix == 'task':
        pass
    Group(group).discard(message.reply_channel)
