FROM alpine:3.6

# install dependencies
RUN apk --no-cache add py-twisted py2-pip && \
    pip2 install incremental constantly packaging

# copy code
COPY . /opt/netflix-no-ipv6-dns-proxy/

# overwrite default config with docker default
COPY config.py.docker /opt/netflix-no-ipv6-dns-proxy/config.py

EXPOSE 53

WORKDIR /opt/netflix-no-ipv6-dns-proxy/
ENTRYPOINT ./server.py
