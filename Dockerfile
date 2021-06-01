FROM alpine
MAINTAINER feloeht

RUN set -xe \
    && apk add --no-cache --purge -uU tzdata dhcp \
    && touch /var/lib/dhcp/dhcpd.leases \
    && rm -rf /var/cache/apk/* /tmp/*

RUN mkdir -p data
COPY data/entrypoint.sh /data/entrypoint.sh
RUN chmod +x /data/entrypoint.sh

EXPOSE 67/udp

ENTRYPOINT ["/data/entrypoint.sh"]
