FROM alpine

LABEL "fr.esieespace.saferouter"="SAFEROUTER"
LABEL fr.esieespace.saferouter.image.authors="theo.lefevre@edu.esiee.fr"

RUN set -xe \
    && apk add --no-cache --purge -uU tzdata dhcp \
    && touch /var/lib/dhcp/dhcpd.leases \
    && rm -rf /var/cache/apk/* /tmp/*

RUN mkdir -p dhcp
COPY src/entrypoint.sh /dhcp/entrypoint.sh
RUN chmod +x /dhcp/entrypoint.sh

EXPOSE 67/udp

ENTRYPOINT ["/dhcp/entrypoint.sh"]
