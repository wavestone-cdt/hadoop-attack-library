CVE-2016-4947 - User enumeration
================================

Description
-----------
Cloudera HUE =< 3.9.0 is vulnerable to an open redirection in the hidden `next` parameter of the login form:
```
http://<cloudera_HUE_IP>:8888/accounts/login/?next=//google.fr
```