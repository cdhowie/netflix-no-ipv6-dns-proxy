#!/bin/env python

from twisted.internet import reactor, defer
from twisted.names import client, dns, error, server

class NoAAAAResolver(object):
    def __shouldForward(self, query):
        if query.type == dns.AAAA and (query.name.name == 'netflix.com' or query.name.name.endswith('.netflix.com')):
            return False

        return True

    def query(self, query, timeout=None):
        if self.__shouldForward(query):
            return defer.fail(error.DomainError())
        else:
            return defer.succeed(([], [], []))

def main():
    factory = server.DNSServerFactory(
        clients=[NoAAAAResolver(), client.Resolver(servers=[('127.0.0.1', 53)])]
    )

    protocol = dns.DNSDatagramProtocol(controller=factory)

    reactor.listenUDP(53, protocol)
    reactor.listenTCP(53, factory)

    reactor.run()

if __name__ == '__main__':
    raise SystemExit(main())
