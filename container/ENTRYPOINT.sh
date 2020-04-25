#!/usr/bin/env bash

service openvswitch-switch start
ovs-vsctl set-manager ptcp:6640

service openvswitch-switch stop

bash -c "python3 /root/CS-425-PROTOTYPE/gui.py"

exit
