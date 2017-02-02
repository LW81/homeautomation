The homeautomation setup consists of various components.
These are:

* home-automation-bridge
* wiringPi
* raspberry-remote
* ha.py


Here are some short instructions on how to setup these components:

## home-automation-bridge setup instuctions
See https://github.com/bwssytems/ha-bridge

ATTENTION: This requires JDK 1.8 to run

Then run it using : java -jar ha-bridge-3.5.1.jar


###For running ha-bridge as a systemd service, use the following template:

```
[Unit]
Description=HA Bridge
Wants=network.target
After=network.target

[Service]
Type=simple
WorkingDirectory=[WORKING_DIR]
ExecStart=/usr/bin/java -jar -Dconfig.file=[habridge.config] [ha-bridge-3.5.1.jar]
User=[USER_TO_RUN_AS]

[Install]
WantedBy=multi-user.target
```


## raspberry-remote setup instructions

sudo apt-get update

sudo apt-get install git-core

git clone git://github.com/xkonni/raspberry-remote.git

cd raspberry-remote

make send

cp send /usr/local/bin/



## wiringPi setup instructions

sudo apt-get update

sudo apt-get install git-core

git clone git://git.drogon.net/wiringPi

cd wiringPi

./build
