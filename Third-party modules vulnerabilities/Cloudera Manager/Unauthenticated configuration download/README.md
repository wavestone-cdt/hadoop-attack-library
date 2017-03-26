Unauthenticated configuration download
======================================

Description
-----------
Cloudera Manager allows to **download module configurations without authentication** by iterating on the module index (integer starting from 1) through the following GET request:
```
http://<cloudera_manager_IP>:7180/cmf/services/<service_id_to_iterate>/client-config
```
This finding may not constitute a vulnerability by itself as:
  * This behaviour can be disallowed by requiring authentication (cf. [`client_config_auth`](http://www.cloudera.com/documentation/enterprise/5-6-x/topics/cm_props_cmserver.html))
  * Cluster configuration can also be downloaded on a [multiple Hadoop WebUI](../../Getting%20the%20target%20environment%20configuration#where-to-get-the-parameter-values-)