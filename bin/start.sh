#!/bin/bash
umask 002

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. && pwd )"
PID_FILE="$ROOT_DIR/cherrypy.pid"
touch $PID_FILE
PID=`cat $PID_FILE`


if [ "$PID" != "" ] && ps -p $PID > /dev/null
then

	echo "Error: CherryPy already running as pid $PID"

else

	cd $ROOT_DIR
	nohup python $ROOT_DIR/src/main.py --env prod --numTorInstances 16 >> stdout.log 2>> stderr.log &
	PID=$!
	echo $PID > $PID_FILE
	echo "CherryPy started as PID $PID"

fi
