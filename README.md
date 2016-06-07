# netflix-no-ipv6-dns-proxy

This is a DNS server that intentionally returns an empty result set for any
AAAA query for netflix.com or any subdomain thereof.  The intent is to force
Netflix to use IPv4 in cases where Netflix has blocked IPv6 access --
specifically, for [Hurricane Electric users who find Netflix giving them the
error](https://forums.he.net/index.php?topic=3564.0):

> You seem to be using an unblocker or proxy. Please turn off any of these
> services and try again. For more help, visit netflix.com/proxy.

Note that this server **does not** in any way circumvent Netflix's block
against these IPv6 address ranges; all it does is force Netflix to use the IPv4
Internet.

I also considered null-routing the Netflix IPv6 address ranges, but many (all?)
Netflix services are deployed in Amazon Web Services, so there's no good way to
reliably null-route Netflix without null-routing all of AWS.  Dealing with the
problem in the DNS process allows us to precisely block exactly what we want
blocked (\*.netflix.com) and nothing that we don't want blocked.

## Dependencies

The only dependency is Twisted Names for Python.

## Configuration

Open `server.py` and configure the `OPTIONS` dict according to the comments.
Here you will be able to configure which address and port this server binds to,
as well as which DNS server it will forward requests to.

Note that if you are using dnsmasq and its built-in DHCP server, and you
reconfigure it to listen on a port other than 53 for DNS, it will stop
advertising itself as a DNS server to DHCP clients.  Put `dhcp-option=6,$IP` in
`dnsmasq.conf` (changing `$IP` to the server's LAN IP) to fix this.  Note that
this will not work when dnsmasq is serving multiple different DHCP ranges,
unless you use an IP address that is reachable from all of those networks.

## Installation

Clone this repository into `/opt/netflix-no-ipv6-dns-proxy`.  (You can clone as
any user, but the server must be run as root in order to bind to port 53.)

Run the following commands to install the systemd service:

    ln -s /opt/netflix-no-ipv6-dns-proxy/netflix-no-ipv6-dns-proxy.service /etc/systemd/system/
    systemctl enable netflix-no-ipv6-dns-proxy.service
    systemctl start netflix-no-ipv6-dns-proxy.service
