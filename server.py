#!/usr/bin/env python

from config import OPTIONS

from twisted.internet import reactor, defer
from twisted.names import client, dns, error, server

class BlockNetflixAAAAResolver(object):
    def __shouldBlock(self, query):
        parts = query.name.name.split(b'.')
        if len(parts) < 2:
            return False
        penultimateDomainPart = parts[-2]

        return query.type == dns.AAAA and penultimateDomainPart in (b'netflix', b'nflximg', b'nflxext', b'nflxvideo', b'nflxso')

    def query(self, query, timeout=None):
        if self.__shouldBlock(query):
            results = []

            blackhole = OPTIONS.get('blackhole', None)
            if blackhole is not None:
                results.append(
                    dns.RRHeader(
                        name=query.name.name,
                        type=dns.AAAA,
                        payload=dns.Record_AAAA(address=blackhole)
                    )
                )

            return defer.succeed((results, [], []))
        else:
            return defer.fail(error.DomainError())

def main():
    factory = server.DNSServerFactory(
        clients=[
            BlockNetflixAAAAResolver(),
            client.Resolver(
                servers=OPTIONS.get('upstream-dns', None),
                resolv=OPTIONS.get('resolv-conf', None)
            )
        ]
    )

    protocol = dns.DNSDatagramProtocol(controller=factory)

    reactor.listenUDP(OPTIONS['listen-port'], protocol, interface=OPTIONS['listen-address'])
    reactor.listenTCP(OPTIONS['listen-port'], factory, interface=OPTIONS['listen-address'])

    reactor.run()

if __name__ == '__main__':
    raise SystemExit(main())
