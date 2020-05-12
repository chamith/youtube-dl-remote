#! /bin/bash

SRC_NAME=app.py
SCRIPT_DIR=$(dirname "$0")
BIN_DIR=/usr/local/bin
BIN_FILE_TARGET=$BIN_DIR/youtube-dl-remote
CONFIG_DIR=$HOME/.youtube-dl-remote
CONFIG_FILE=$CONFIG_DIR/settings.conf

if [ -f "$BIN_FILE_TARGET" ]; then
    echo "removing existing binary files"
    rm $BIN_FILE_TARGET
fi

cp $SCRIPT_DIR/$SRC_NAME $BIN_FILE_TARGET

if [ ! -d "$CONFIG_DIR" ]; then
    echo "creating app settings directory"
    mkdir $CONFIG_DIR
fi

if [ ! -f "$CONFIG_FILE" ]; then
    echo "creating the config file"
    cp $SCRIPT_DIR/conf.tmpl $CONFIG_FILE
fi

apt install python3-pip -y
pip3 install -r $SCRIPT_DIR/requirements.txt
