#!/bin/sh

# Initialize the lease file if it doesn't exist.
touch /var/lib/dhcp/dhcpd.leases

# Start server.
dhcpd -cf /etc/dhcp/dhcpd.conf -lf /var/lib/dhcp/dhcpd.leases --no-pid -4 -f
