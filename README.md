## Helpful notes for MPC


## Viff: scratch examples using viff.  
* places to look in the code
* [Viff overview](http://viff.dk/api/index.html)



# Viff Scratch Messing Around

* modifying the millionaires problem to see what is going on.
* copy `battleship.py` into your `viff/apps/` directory. 
```
$> ln -s ic3_mpc/battleship.py ic3_mpc/launch_ship.sh {your_viff_dir}/apps/battleship.py
$> ln -s ic3_mpc/launch_ship.sh {your_viff_dir}/apps/launch_ship.sh
$> cd viff/apps
$> ./launch_ships.sh
```

# generate the config file 
```
$> python generate-config-files.py -n 3 -t 1 localhost:9001 localhost:9002 localhost:9003
```

# run scratch project
```
$> python battleship.py --no-ssl player-1.ini
$> python battleship.py --no-ssl player-2.ini
$> python battleship.py --no-ssl player-3.ini
```

# running the main loop
_Work in progress_

```bash
$ pip install future
```

```bash
$ python main_loop.py
Welcome to the MPC Battleship game. Type help or ? to list commands.

(battleship)
```

```bash
(battleship) help

Documented commands (type help <topic>):
========================================
board  help

Undocumented commands:
======================
recv_attack  send_attack  show_board

(battleship)
```

```bash
$ python main_loop.py
(battleship) board
carrier (length 5) default: 0 0 0? 0 3 3
...
```

# using docker-compose

In one shell, generate config files for players:

```bash
$ docker-compose up config
```

In 3 seperate shells:

player 1:

```bash
$ docker-compose run --rm --name p1 p1 bash
(container) python number_shoot_out.py --no-ssl player-1.ini
```

player 2:

```bash
$ docker-compose run --rm --name p2 p2 bash
(container) python number_shoot_out.py --no-ssl player-2.ini
```

player 3:

```bash
$ docker-compose run --rm --name p3 p3 bash
(container) python number_shoot_out.py --no-ssl player-3.ini
```
