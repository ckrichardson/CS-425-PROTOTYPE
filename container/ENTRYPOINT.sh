#!/bin/bash

service openvswitch-switch start
ovs-vsctl set-manager ptcp:6640

bash -c "python3 /root/CS-425-PROTOTYPE/gui.py"

service openvswitch-switch stop
