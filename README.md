This is a DNS server that intentionally returns an empty result set for any AAAA query for netflix.com or any subdomain thereof.  The intent is to force Netflix to use IPv4 in cases where Netflix has blocked IPv6 access -- specifically, for Hurricane Electric users who find Netflix giving them the error:

> You seem to be using an unblocker or proxy. Please turn off any of these services and try again. For more help, visit netflix.com/proxy.

Note that this server **does not** in any way circumvent Netflix's block against these IPv6 address ranges; all it does is force Netflix to use the IPv4 Internet.
