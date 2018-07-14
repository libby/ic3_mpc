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
$> python generate-config-files.py -n 3 -t 1 localhost:9001 localhost:9002 localhost:9003

# run scratch project
$> python battleship.py --no-ssl player-1.ini
$> python battleship.py --no-ssl player-2.ini
$> python battleship.py --no-ssl player-3.ini
```

