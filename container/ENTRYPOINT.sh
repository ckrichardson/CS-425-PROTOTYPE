#!/bin/bash

#service openvswitch-switch start
#service ovs-vswitchd start
#ovs-vsctl set-manager ptcp:6640

/usr/share/openvswitch/scripts/ovs-ctl start

bash -c "python3 -m /root/CS-425-PROTOTYPE/gui.py"

service openvswitch-switch stop
