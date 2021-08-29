#!/bin/bash
sudo apt-get install mosquitto
sudo apt-get install mosquitto-clients
python3 -m venv	venv
source venv/bin/activate
pip3 install -r requirements.txt
