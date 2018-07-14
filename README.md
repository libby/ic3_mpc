## Helpful notes for MPC


## Viff: scratch examples using viff.  
* places to look in the code
* [Viff overview](http://viff.dk/api/index.html)



# Viff Scratch Messing Around

* modifying the millionaires problem to see what is going on.
* copy `battleship.py` into your `viff/apps/` directory. 

```
# generate the config file for the millionaires game
$> cd viff/apps 
$> python generate-config-files.py -n 3 -t 1 localhost:9001 localhost:9002 localhost:9003

# run scratch project
$> python battleship.py --no-ssl player-1.ini
$> python battleship.py --no-ssl player-2.ini
$> python battleship.py --no-ssl player-3.ini
```

