Configuration file world readable
=================================

Description
-----------
The `hue.ini` configuration file is by default **accessible to anyone** with the `other` permission set to `read`:
```
$ ls -al /etc/hue/conf/hue.ini 
-rw-rw-r-- 1 root root 22813 Nov 18  2015 /etc/hue/conf/hue.ini
```
  
Several account credentials can be found in that configuration file such as:
  * **Database account**: this might be the most interesting post-exploitation move to spoof an user identity on the datalake as [session cookies are stored in the database](../Session cookies stored in the database/)
  * LDAP bind account
  * SMTP service account
  * Kerberos keytab
  * Default user credentials
  * etc.
  
  
References
----------
  * [Issue on the HUE repository](https://github.com/cloudera/hue/issues/446)