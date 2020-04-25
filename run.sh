#!/usr/bin/env bash
sudo docker run -it --rm --privileged -e DISPLAY \                                                                                                                     (base) 
                            -v /tmp/.X11-unix:/tmp/.X11-unix \
                            -v /lib/modules:/lib/modules \
                            sdn-toolkit