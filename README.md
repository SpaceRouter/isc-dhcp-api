# isc-dhcp-api

PYTHON REST API for isc-dhcp-server (soon using jwt authentication)

Run:
----
    python isc-dhcp-api.py

MAC Encode :
---------
    76:e6:a2:4b:b2:62 --> 76%3Ae6%3Aa2%3A4b%3Ab2%3A62 (: --> %3A)

API List :
---------

**ADD static Leases:**
Create a static DHCP lease

    curl -d "hostname=test&mac=76%3Ae6%3Aa2%3A4b%3Ab2%3A62&ip=192.168.1.51" -X POST http://localhost:8080/admin/addfix

**DELETE static Leases:**
Delete a static DHCP lease

    curl -d "hostname=test&mac=76%3Ae6%3Aa2%3A4b%3Ab2%3A62" -X POST http://localhost:8080/admin/deletefix

**Data:**
Retrieve data regarding static leases, current leases, free leases.

    curl -X GET http://localhost:8080/data.json

**Restart:**
Restarting the isc-dhcp-server service

    curl -X POST http://localhost:8080/admin/restart