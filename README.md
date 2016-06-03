# fix-netflix-dns

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

## Installation

Clone this repository into `/opt/fix-netflix-dns`.  (You can clone as any user,
but the server must be run as root in order to bind to port 53.)

Configure your existing DNS server/forwarder to listen on port 10053, and
restart it.

Run the following commands to install the systemd service:

    cd /etc/systemd/system
    ln -s /opt/fix-netflix-dns/fix-netflix-dns.service
    systemctl enable fix-netflix-dns.service
    systemctl start fix-netflix-dns.service
