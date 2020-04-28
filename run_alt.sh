#!/bin/bash
sudo docker run --rm --privileged -it \
   --user=root \
   --env="DISPLAY" \
   --workdir=/app \
   --volume="$PWD":/app \
   --volume="/etc/group:/etc/group:ro" \
   --volume="/etc/passwd:/etc/passwd:ro" \
   --volume="/etc/shadow:/etc/shadow:ro" \
   --volume="/etc/sudoers.d:/etc/sudoers.d:ro" \
   --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
   --volume="/lib/modules:/lib/modules" \
   --volume="fuzzer_logs:/root/CS-425-PROTOTYPE/fuzzer_logs:rw" \
   sdn-toolkit