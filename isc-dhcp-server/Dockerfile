FROM alpine:latest

LABEL "space.opengate.vendor"="SpaceRouter"
LABEL org.opencontainers.image.source https://github.com/SpaceRouter/isc-dhcp-api
LABEL space.opengate.image.authors="theo.lefevre@edu.esiee.fr"

RUN apk add --no-cache --purge -uU tzdata dhcp
RUN touch /var/lib/dhcp/dhcpd.leases
RUN rm -rf /var/cache/apk/* /tmp/*

RUN mkdir -p dhcp
COPY entrypoint.sh /dhcp/entrypoint.sh
RUN chmod +x /dhcp/entrypoint.sh

EXPOSE 67/udp

ENTRYPOINT ["sh", "/dhcp/entrypoint.sh"]
