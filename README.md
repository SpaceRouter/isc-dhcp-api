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

**Data:**

Retrieve data regarding static leases, current leases, free leases.

    curl -X GET http://localhost:8080/data.json

Return example:

```
{
   "fixed":{
      
   },
   "staging":{
      "192.168.1.51":{
         "ends":"2021/05/31 20:20:48",
         "starts":"2021/05/31 20:10:48",
         "has_name":false,
         "hostname":"saferouteur-Standard-PC-i440FX-PIIX-1996",
         "binding":"active",
         "state":true,
         "mac":"76:e6:a2:4b:b2:62"
      },
      "192.168.1.50":{
         "ends":"2021/05/31 20:18:47",
         "starts":"2021/05/31 20:08:47",
         "has_name":false,
         "hostname":"Safe-Router-LAN",
         "binding":"active",
         "state":true,
         "mac":"4e:65:fd:62:c7:31"
      }
   },
   "free":{
      
   }
}
```

**Restart:**

Restarting the isc-dhcp-server service

    curl -X POST http://localhost:8080/restart
