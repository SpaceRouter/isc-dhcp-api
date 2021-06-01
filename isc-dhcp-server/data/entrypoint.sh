#!/bin/sh

# Initialize the lease file if it doesn't exist.
#touch /data/dhcpd/dhcpd.leases

# Start devpi-server.
dhcpd -cf /data/dhcp/dhcpd.conf -lf /data/dhcp/dhcpd.leases --no-pid -4 -f
