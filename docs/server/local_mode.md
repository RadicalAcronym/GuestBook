GUESTBOOK is root directory for this.
* GuestBookServer directory is for the webservice that will accept and process guest videos

    * serverapp is where the server code is
    * devel is where the docker stuff is to create the local delvelopment environment
    * 


for local development you start the server by 
```
cd devel
docker-compose up
```
Then in another window you can run
```
cd devel
docker-compose -f docker-compose-devel.yml run gbdevel /bin/bash
```

where you can do things like 
```
python manage.py collectstatic
```


