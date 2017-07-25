#!/usr/bin/env python
# coding=utf-8
import asyncore
import socket
import struct
import threading

import gevent
import zerorpc
from django.conf import settings
from django.core.management.base import BaseCommand

if settings.TEST_SERVICE_SETTINGS:
    TEST_SERVICE_SETTINGS = settings.TEST_SERVICE_SETTINGS
else:
    TEST_SERVICE_SETTINGS = {}
RPC_ADDRESS = TEST_SERVICE_SETTINGS.get('RPC_ADDRESS', 'tcp://localhost:9001')
SERVICE_HOST = TEST_SERVICE_SETTINGS.get('SERVICE_HOST', '127.0.0.1')
SERVICE_PORT = TEST_SERVICE_SETTINGS.get('SERVICE_PORT', 8005)


class GlobalInfo:
    def __init__(self, initial_flag, function_id, send_flag, socket_word, receive_data):
        self.initial_flag = initial_flag
        self.function_id = function_id
        self.send_flag = send_flag
        self.socket_word = socket_word
        self.receive_data = receive_data


class CustomHandler(asyncore.dispatcher_with_send):
    def __init__(self, global_info, **kwargs):
        super(CustomHandler, self).__init__(**kwargs)
        self.global_info = global_info

    def handle_read(self):
        recv_data = self.recv(1037)
        if len(recv_data) == 1037:
            head, function_id, length, data, check = struct.unpack('III1024ss', recv_data)
            gevent.sleep(0.5)
            if head == 0xaaaaaaaa:
                if (function_id & 0xff000000) == 0x0:
                    pass
                if (function_id & 0xff000000) == 0xE0000000:
                    pass
                if (function_id & 0xff000000) == 0xF0000000:
                    pass
                if (function_id >= 0x01000000) & (function_id <= 0xDFFFFFFF):
                    data_str = data[0:length - 1]
                    self.global_info.receive_data[repr(function_id)] = data_str


class CustomServer(asyncore.dispatcher):
    def __init__(self, host, port, global_info):
        asyncore.dispatcher.__init__(self)
        self.handler = None
        self.global_info = global_info
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        print('server address is %s' % host)
        print('server address is %d' % port)

    def handle_accept(self):
        conn, address = self.accept()

        socket_word = self.global_info.socket_word
        print('Incoming connection from %s' % repr(address))
        self.global_info.initial_flag = 1
        cut_flag = 0
        repr_address = repr(address)
        for i in range(1, 10):
            if repr_address[-i] == ',':
                cut_flag = -i
                break
        repr_address = repr_address[1:cut_flag]
        socket_word[repr_address] = conn
        self.handler = CustomHandler(sock=conn, global_info=self.global_info)


class EchoServerThread(threading.Thread):
    def __init__(self, host, port, global_info):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.global_info = global_info

    def run(self):
        server = CustomServer(host=self.host, port=self.port, global_info=self.global_info)
        asyncore.loop()


class TestServer:
    def __init__(self, host, port, global_info):
        self.initial_flag = 0
        self.function_id = 0
        self.send_flag = 0
        self.socket_word = {}
        self.receive_data = {}
        self.global_info = global_info
        self.thread = EchoServerThread(host=host, port=port, global_info=self.global_info)

    def run(self):
        self.thread.daemon = True
        self.thread.start()

    def socket_write(self, function_id, address):
        head = 0xa5a5a5a5
        length = 0
        data = b'0' * 1024
        checksum = bytes(str(function_id), encoding="utf8")
        c = self.socket_word[repr(address)]
        socket_pack = struct.pack('III1024ss', head, function_id, length, data, checksum)
        c.sendall(socket_pack)


class Command(BaseCommand):
    help = '启动615的服务'

    def handle(self, *args, **options):
        try:
            global_info = GlobalInfo(0, 0, 0, {}, {})
            server = TestServer(host=SERVICE_HOST, port=SERVICE_PORT, global_info=global_info)
            server.run()
            s = zerorpc.Server(server)
            s.bind(RPC_ADDRESS)
            self.stdout.write(self.style.SUCCESS('615服务启动：{0}'.format(RPC_ADDRESS)))
            s.run()
        except BaseException as e:
            self.stdout.write(self.style.ERROR('{0}'.format(e)))
