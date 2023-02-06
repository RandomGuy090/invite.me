#!/bin/sh
app="invite_me"
port="8080"
docker build -t ${app} .
docker run -d -p 8080:${port} \
  --name ${app}\
  -e FLASK_APP=${app}\
  -e FLASK_RUN_PORT=${port}\
  -v $PWD:/app ${app}