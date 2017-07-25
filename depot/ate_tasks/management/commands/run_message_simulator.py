#!/usr/bin/env python
# coding=utf-8
import json
import random

from channels import Group
from django.core.management.base import BaseCommand
from gevent import sleep

import ate_tasks.models as models


class Command(BaseCommand):
    help = '启动总线数据生成器'

    # FIXME 需要根据不同的总线生成数据，不过这个不着急
    def handle(self, *args, **options):
        try:
            while True:
                sleep(0.5)
                for monitor in models.Monitor.objects.filter(is_running=True):
                    group = 'monitor-{uuid}'.format(uuid=monitor.uuid)
                    message = {'id': random.randint(25, 29)}
                    message_content = [random.randint(0, 100) for i in range(random.randint(0, 20))]
                    message['length'] = len(message_content)
                    message['origin'] = '-'.join(map(hex, message_content))
                    message['bus_type'] = 'Test'
                    content = {'message_type': 'message', 'message': message}
                    models.MonitorRecord.objects.create(content=json.dumps(content, ensure_ascii=False))
                    if monitor.rules != '':
                        messages = list(map(int, monitor.rules.split('-')))
                        if message['id'] in messages:
                            Group(group).send({'text': json.dumps(content, ensure_ascii=False)})
                    else:
                        Group(group).send({'text': json.dumps(content, ensure_ascii=False)})

        except BaseException as e:
            self.stdout.write(self.style.ERROR('{0}'.format(e)))
