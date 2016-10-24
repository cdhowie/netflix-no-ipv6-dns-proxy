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

The Netflix apps for Chromecast and Android have started **ignoring the DNS
servers announced over DHCP and will send queries directly to 8.8.8.8 and/or
8.8.4.4**. If you are running this proxy on your network's default gateway,
simply configure the LAN-facing interface with these addresses to force all
queries to them to be handled by the proxy. If you are running the DNS proxy
on another box, you will have to configure your router to NAT DNS requests to
these addresses to that other box.

Alternatively, if you block the Google Public DNS servers at the router level
this will force a Chromecast device to fallback to the DNS servers pushed via DHCP.

An example of achieving this with `iptables`:

```
iptables -I FORWARD --destination 8.8.8.8 -j REJECT
iptables -I FORWARD --destination 8.8.4.4 -j REJECT
```

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

    cp /opt/netflix-no-ipv6-dns-proxy/netflix-no-ipv6-dns-proxy.service /etc/systemd/system/
    systemctl enable netflix-no-ipv6-dns-proxy.service
    systemctl start netflix-no-ipv6-dns-proxy.service

If you don't want to have to keep the unit file up to date manually, you can
symlink it (`ln -s`) if your version of systemd works with symlinked unit
files, or hardlink it if `/opt/netflix-no-ipv6-dns-proxy` and
`/etc/systemd/system` exist on the same volume.

If you're using a system that's not using systemd, install the init script and start the service as follows:

    cp netflix-no-ipv6-dns-proxy.init /etc/init.d/netflix-no-ipv6-dns-proxy
    update-rc.d -n netflix-no-ipv6-dns-proxy defaults
    service netflix-no-ipv6-dns-proxy start

If you're using launchd (eg: macOS), install the launchd.plist and load the service as follows:

    sudo cp com.github.cdhowie.netflix-no-ipv6-dns-proxy.plist /Library/LaunchDaemons
    sudo launchctl load -w /Library/LaunchDaemons/com.github.cdhowie.netflix-no-ipv6-dns-proxy.plist
