#!/bin/bash

case `uname` in
  CYGWIN*)
    CP=$( echo `dirname $0`/../lib/*.jar . | sed 's/ /;/g')
    ;;
  *)
    CP=$( echo `dirname $0`/../lib/*.jar . | sed 's/ /:/g')
esac
#echo $CP

# Find Java
if [ "$JAVA_HOME" = "" ] ; then
    JAVA="java -server"
else
    JAVA="$JAVA_HOME/bin/java -server"
fi

# Set Java options
#if [ "$JAVA_OPTIONS" = "" ] ; then
#    JAVA_OPTIONS="-Xms32m -Xmx512m"
#fi

# Launch the application
JAVA_OPTIONS="$JAVA_OPTIONS -Xms4096m -Xmx4096m -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=7199 -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.local.only=false"
TITAN_PID="./titan.pid"
TITAN_OUT="./titan.out"

if [ ! -z "$TITAN_PID" ]; then
  if [ -f "$TITAN_PID" ]; then
    if [ -s "$TITAN_PID" ]; then
      echo "Existing PID file found during start."
      if [ -r "$TITAN_PID" ]; then
        PID=`cat "$TITAN_PID"`
        ps -p $PID >/dev/null 2>&1
        if [ $? -eq 0 ] ; then
          echo "Titan appears to still be running with PID $PID. Start aborted."
          exit 1
        else
          echo "Removing/clearing stale PID file."
          rm -f "$TITAN_PID" >/dev/null 2>&1
          if [ $? != 0 ]; then
            if [ -w "$TITAN_PID" ]; then
              cat /dev/null > "$TITAN_PID"
            else
              echo "Unable to remove or clear stale PID file. Start aborted."
              exit 1
            fi
          fi
        fi
      else
        echo "Unable to read PID file. Start aborted."
        exit 1
      fi
    else
      rm -f "$TITAN_PID" >/dev/null 2>&1
      if [ $? != 0 ]; then
        if [ ! -w "$TITAN_PID" ]; then
          echo "Unable to remove or write to empty PID file. Start aborted."
          exit 1
        fi
      fi
    fi
  fi
fi

touch "$TITAN_OUT"

$JAVA $JAVA_OPTIONS -cp $CP:$CLASSPATH com.thinkaurelius.titan.tinkerpop.rexster.RexsterTitanServer "$@" >> "$TITAN_OUT" 2>&1 &
  
if [ ! -z "$TITAN_PID" ]; then
  echo $! > "$TITAN_PID"
fi

