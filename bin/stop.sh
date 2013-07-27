#!/bin/bash

#!/bin/bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. && pwd )"
PID_FILE="$ROOT_DIR/cherrypy.pid"
touch $PID_FILE
PID=`cat $PID_FILE`

if [ "$PID" != "" ] && ps -p $PID > /dev/null
then
	
	echo "Stopping CherryPy..."
	kill $PID
	exit 0

else

	echo "ERROR: cherrypy is not currently running."
	exit 1
fi
