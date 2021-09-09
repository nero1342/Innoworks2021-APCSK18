#!/bin/bash -x
PWD=`pwd`
echo $PWD
activate () {
    . $PWD/$1/bin/activate
}

activate pytorch19

python services/app.py & 
p1pid=$!

python services/app_transportation.py & 
p2pid=$!

activate pytorch14
python services/app_pedestron.py &
p3pid=$!

echo $p1pid $p2pid $p3pid
wait
kill $p1pid $p2pid $p3pid



