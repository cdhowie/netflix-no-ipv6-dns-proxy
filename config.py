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
    #'resolv-conf': '/etc/resolv.conf',

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