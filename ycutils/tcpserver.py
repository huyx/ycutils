# -*- coding: utf-8 -*-
from twisted.internet import protocol, reactor
from twisted.python import usage
import itertools
import sys
import time
import platform

u"""TCP 测试服务器

命令行参数说明:

    -l --listen    监听端口
    -t --type      服务器类型: (n)one, (e)cho, (h)ttp, (d)atafile
        n          None 服务器，不回应任何东西
        e          Echo 服务器，发送什么回应什么
        h          Http 服务器，发送简单的 http 响应
        d          连接后发送指定的数据文件
    -d --datafile  服务器类型为 d 时，用于指定数据文件
    -c --close     关闭连接的时机, 0: 连接后直接关闭, 1: 发送数据后关闭, 2: 不关闭
    -v --verbose   显示详细信息
    -V --version   显示版本信息
"""

def dolog(*args):
    print time.strftime("%Y-%m-%d %H:%M:%S"), " ".join(map(str, args))
    sys.stdout.flush()

VERSION = "0.1"
HTTP_RESPONSE = u"HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\n\r\n简单就是美".encode("utf-8")

class Options(usage.Options):
    optParameters = [
        ["listen", "l", 9999, u"监听端口", int],
        ["type", "t", "n", u"服务器类型: (n)one, (e)cho, (h)ttp, (d)atafile"],
        ["datafile", "d", None, u"服务器类型为 d 时，用于指定数据文件"],
        ["close", "c", 2, u"关闭连接的时机, 0: 连接后直接关闭, 1: 发送数据后关闭, 2: 不关闭", int],
    ]

    optFlags = [
        ["version", "V", u"显示版本信息"],
    ]


    def __init__(self):
        usage.Options.__init__(self)
        self["verbose"] = 0

    def opt_verbose(self):
        u"""显示详细信息"""
        self["verbose"] += 1

    opt_v = opt_verbose

    def postOptions(self):
        if self["version"]:
            print VERSION
            sys.exit(0)

        if self["type"] == "d" and not self["datafile"]:
            print u"type 为 d 时必须指定 datafile"
            sys.exit(1)

class ServerProtocol(protocol.Protocol):
    _seqno = itertools.count(1).next

    def __init__(self, options):
        self.options = options
        self.seqno = self._seqno()
        self.repstr = "#%d" % self.seqno

    def __str__(self):
        return self.repstr

    def connectionMade(self):
        dolog(self, "connectionMade")
        if self.options["close"] == 0:
            self.transport.loseConnection()

    def dataReceived(self, data):
        dolog(self, "R:", repr(data))
        if self.options["type"] == "e":
            self.write(data)
        elif self.options["type"] == "h":
            self.write(HTTP_RESPONSE)
        elif self.options["type"] == "d":
            self.write(open(self.options["datafile"], "rb").read())
        else:
            pass
        if self.options["close"] == 1:
            self.transport.loseConnection()

    def write(self, data):
        dolog(self, "W:", repr(data))
        self.transport.write(data)

    def connectionLost(self, reason):
        dolog(self, "connectionLost:", reason.getErrorMessage())

class Server(protocol.ServerFactory):
    def __init__(self, options):
        self.options = options

    def buildProtocol(self, addr):
        return ServerProtocol(self.options)

def main(options):
    reactor.listenTCP(options["listen"], Server(options))
    reactor.run()

def setdefaultencoding():
    encoding = "utf-8"
    if platform.system() == "Windows":
        encoding = "gbk"
    reload(sys)
    sys.setdefaultencoding(encoding)

if __name__ == '__main__':
    setdefaultencoding()
    options = Options()
    options.parseOptions()
    main(options)
