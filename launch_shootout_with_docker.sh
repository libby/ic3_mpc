#!/bin/bash

docker-compose up config
PROGRAM="number_shoot_out.py --no-ssl"
set -x
tmux new -s battle "docker-compose run --rm --name p1 p1 python ${PROGRAM} player-1.ini; bash" \; \
     splitw -h -p 50 "docker-compose run --rm --name p2 p2 python ${PROGRAM} player-2.ini; bash" \; \
     splitw -v -p 50 "sleep 2; docker-compose run --rm --name p3 p3 python ${PROGRAM} player-3.ini; bash" \; 
