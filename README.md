#Rbx-1 Comand and Control

This project uses pipenv to handle project depenesies.
Install with:
```sh
$ pip install --user pipenv
```

Then you can just run the server on with:
```sh
$ pipenv run python server.py
```
This will download and install missing pytion pacages to its own enviropment before running the server.

The server will:
* Test if robot is conected localy. (todo)
* Will run in testmode if not found. (todo)
* Will lissen on conections from 0.0.0.0:8080.

Just browse to http://ip:8080/ to use web ui.