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

    # Specify one or more servers to proxy to.
    # 'upstream-dns': [('::1', 10053)],

    # Specify a resolv.conf file from which to read upstream nameservers.
    # 'resolv-conf': '/etc/resolv.conf',
}

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
        clients=[
            NoAAAAResolver(),
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
