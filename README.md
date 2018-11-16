#Rbx-1 Command and Control
Robotic arm controller and web server run on a Raspberry Pi. Allows clients to control arm from a web UI with a game pad controller.

If application is started on anything else than a RPi the web UI and game pad functionality can be tested, with a mock implementation of the robot controller.

This project uses pipenv to handle project dependencies.
Install with:
```sh
$ pip install --user pipenv
```

Then you can just run the server on with:
```sh
$ pipenv run python server.py
```

This will download and install missing python packages to its own environment before running the server.

The server will:
* Test if robot is conected locally. (todo)
* Will run in test mode if not found.
* Will listen to connections from 0.0.0.0:8080.

Just browse to http://ip:8080/ to use web UI.