#!/bin/bash
start_time=`date +%s`
sudo docker build -t sdn-toolkit container/
end_time=`date +%s`
build_time=$((end_time-start_time))
echo "Build took $build_time seconds!"
