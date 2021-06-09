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

    curl -d "hostname=test&mac=76%3Ae6%3Aa2%3A4b%3Ab2%3A62&ip=192.168.1.51" -X POST http://localhost:8080/addfix

**DELETE static Leases:**

Delete a static DHCP lease

    curl -d "hostname=test&mac=76%3Ae6%3Aa2%3A4b%3Ab2%3A62" -X POST http://localhost:8080/deletefix

**Scope:**

Retrieve data regarding dhcp server configuration.

    curl -X GET http://localhost:8080/scope

Return example:

```
{
   "scope":[
      {
         "end":"192.168.1.150",
         "subnet-mask":"255.255.255.0",
         "start":"192.168.1.10",
         "domain-name":"opengate.lan",
         "domain-name-servers":"192.168.1.1",
         "scope":"192.168.1.0",
         "broadcast-address":"192.168.1.255"
      }
   ]
}
```

**Data:**

Retrieve data regarding static leases, current leases, free leases.

    curl -X GET http://localhost:8080/data

Return example:

```
{
   "free":[
      {
         "ip":"192.168.1.100",
         "starts":"2021/06/01 22:54:39",
         "ends":"2021/06/02 22:54:39",
         "binding":"free",
         "mac":"4a:9a:25:4d:07:69",
         "hostname":"Safe-Router-LAN2"
      }
   ],
   "fixed":[
      {
         "binding":"fixed",
         "hostname":"saferouteur-Standard-PC-i440FX-PIIX-1996",
         "mac":"76:e6:a2:4b:b2:62",
         "ip":"192.168.1.60"
      }
   ],
   "staging":[
      {
         "ip":"192.168.1.50",
         "starts":"2021/06/01 13:01:23",
         "ends":"2021/06/02 13:01:23",
         "binding":"active",
         "mac":"4e:65:fd:62:c7:31",
         "hostname":"Safe-Router-LAN"
      },
      {
         "ip":"192.168.1.51",
         "starts":"2021/06/01 22:54:39",
         "ends":"2021/06/02 22:54:39",
         "binding":"active",
         "mac":"4a:9a:25:4d:07:19",
         "hostname":"Safe-Router-LAN1"
      }
   ]
}
```

**Restart:**

Restarting the isc-dhcp-server service

    curl -X POST http://localhost:8080/restart
