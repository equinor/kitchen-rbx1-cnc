# Rbx-1 Command and Control
Robotic arm controller and web server run on a Raspberry Pi. Allows clients to control RBX1 arm from a web UI with a game pad controller.

If application is started on anything else than a RPi the web UI and game pad functionality can be tested, with a mock implementation of the robot controller.


## Getting started
It utilizes openCV to capture images from the attached cameras. To make it work do:
```sh
$ sudo apt install libatlas3-base libsz2 libharfbuzz0b libtiff5 libjasper1 libilmbase12 libopenexr22 libilmbase12 libgstreamer1.0-0 libavcodec57 libavformat57 libavutil55 libswscale4 libqtgui4 libqt4-test libqtcore4
```

This project uses pipenv to handle project dependencies:
```sh
$ pip3 install --user pipenv
```
Add pipenv to path:
```sh
$ echo 'export PATH=/home/{user}/.local/bin:$PATH' >> ~/.bashrc
```

Install dependencies:
```sh
$ pipenv install
```

Then you can just run the server with:
```sh
$ pipenv run python server.py
```

The server will:
* Test if robot is connected locally.
* Will run in test mode if not found.
* Will listen to connections from 0.0.0.0:8080.

Just browse to http://ip:8080/ to use web UI.

## SlushEngine configuration
[see here](https://github.com/Roboteurs/slushengine)
* pipenv shell
* git clone https://github.com/quick2wire/quick2wire-python-api
* sudo python setup.py install
* git clone https://github.com/Roboteurs/slushengine
* sudo python setup.py install
* pip install RPi.GPIO