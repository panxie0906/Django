# coding=utf-8
import os
import signal
from subprocess import Popen
from sys import executable, stderr, stdin, stdout

import gevent
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Run all commands'
    commands = [
        '{0} manage.py runserver 0.0.0.0:8000'.format(executable),
        '{0} manage.py run_test_engine'.format(executable),
    ]

    def handle(self, *args, **options):
        proc_list = []

        for command in self.commands:
            print("$ " + command)
            proc = Popen(command, shell=True, stdin=stdin, stdout=stdout, stderr=stderr)
            proc_list.append(proc)
        proc_list[0].wait()
