
https://cloud.google.com/sql/docs/postgres/quickstart

from within the gcloud sdk

```
apt update
apt install postgresql-client

gcloud sql connect gbdb1 --user=postgres
```

The password is found in GuestBookServer/devel/envgc.dev

```
\l
```
shows the databases. I think it defaults to postgres, which is what we want.

```
\dt
```
shows the tables in the current database.

then you can do something like

```
SELECT * from hosts_video;
```
to show that table.  Remember the semicolon.



