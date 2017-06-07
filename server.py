#!/usr/bin/env python

OPTIONS = {
    # Port to bind to.
    'listen-port': 53,

    # Address to bind to.  '::' will bind IPv6; make sure bindv6only is 0 in
    # your sysctl configuration for this binding to service IPv4 clients, too.
    # ("cat /proc/sys/net/ipv6/bindv6only" to verify.)
    'listen-address': '::',

    # Here is where you configure what DNS server to proxy to.  You must
    # specify exactly one of the following options; comment out the other.

    # Specify one or more servers to proxy to.  Note that Twisted may not be
    # happy if you use an IPv6 address.
    # 'upstream-dns': [('127.0.0.1', 10053)],

    # Specify a resolv.conf file from which to read upstream nameservers.  As
    # noted above, if you have any upstream IPv6 servers, Twisted may not be
    # happy about that.
    # 'resolv-conf': '/etc/resolv.conf',

    # Set this to an IPv6 address and all blocked queries will return this
    # address instead of an empty result set.  The Android Netflix client has
    # (for me) started getting testy when AAAA queries return nothing.  Set
    # this to an address in an unreachable route to resolve that issue.  I
    # suggest b'100::1' as this is within the RFC6666-specified discard prefix.
    #
    # Run this command on your Linux router to add an unreachable route for the
    # entire discard prefix (100::/64).  Add it to the "up" script for your lo
    # interface if you want it preserved on reboots.
    #
    # # ip route add unreachable 0100::/64
    'blackhole': None,  # b'100::1',
}

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
