Unauthenticated policy download
===============================

Description
-----------
Apache Ranger =< 0.5.2 allows to download policy definitions without authentication through the following GET request:
```
http://<apache_ranger_IP>:6080/service/plugins/policies/download/<policy_name>
```
The prerequisite to exploit this flaw is to know (or guess) the policy name.  
This finding may not constitute a vulnerability by itself, but is equivalent to having access to a network filtering policy: finding holes in policies is then easier for an attacker.  