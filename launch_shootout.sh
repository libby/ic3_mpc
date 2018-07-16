#!/bin/bash

python generate-config-files.py -n 3 -t 1 localhost:9001 localhost:9002 localhost:9003
#PROGRAM_DEBUG="number_shoot_out.py --no-ssl --statistics --deferred-debug"
PROGRAM="battleship.py --no-ssl"
set -x
#tmux new-session "python ${PROGRAM} player-1.ini; bash" \; \
tmux new -s battle "python ${PROGRAM} player-1.ini; bash" \; \
     splitw -h -p 50 "python ${PROGRAM} player-2.ini; bash" \; \
     splitw -v -p 50 "sleep 2; python ${PROGRAM} player-3.ini; bash" \; 
