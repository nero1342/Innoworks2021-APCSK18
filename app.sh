#!/bin/bash -x
PWD=`pwd`
echo $PWD
activate () {
    . $PWD/$1/bin/activate
}

activate pytorch14
python services/app_pedestron.py &

activate pytorch19
python services/app.py & 
python services/app_transportation.py & 

python cameraMonitor.py 


