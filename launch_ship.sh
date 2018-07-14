#!/bin/bash
python generate-config-files.py -n 3 -t 1 localhost:9001 localhost:9002 localhost:9003
PROGRAM="battleship.py --no-ssl --statistics --deferred-debug"
set -x
#python millionaires.py --no-ssl player-1.ini
tmux new-session "python ${PROGRAM} player-1.ini; bash" \; \
     splitw -h -p 50 "python ${PROGRAM} player-2.ini; bash" \; \
     splitw -v -p 50 "python ${PROGRAM} player-3.ini; bash" \; 
