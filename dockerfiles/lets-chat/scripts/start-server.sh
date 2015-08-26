#!/bin/bash

#Extract Mongo credentials from VCAP_SERVICES
TEMP=`python extract-vcap.py mongolab 0 credentials.uri`
if [ "$?" = "0" ]; then
	export LCB_DATABASE_URI=${TEMP}
fi

#Run server
npm start
