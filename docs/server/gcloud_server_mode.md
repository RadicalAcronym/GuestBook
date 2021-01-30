Within GuestBookServer/serverapp there is a file called `app.yaml`. This file contains the configuration parameters for the google app engine.

Since this `app.yaml` file has some secret information, make sure you don't have this in your git repository

To deploy, you can run the command from within the devel directory
```
docker-compose -f docker-compose-gcsdk.yml run sdk
```

This will start a docker container with the google cloud development kit tools. and mount your server code to the /opt/appserver directory within that container.

within the docker terminal, type
```
gcloud init
```
and follow the instructions. our google account is `factoryrdlab@gmail.com` and the cloud project is `thinking-glass-282301`

I've been picking zone us-central1-c for the zone.

To deploy the app, use these commands
```
cd /opt/appserver
gcloud app deploy frontend1/app.yaml backend1/app.yaml 
```






