#!/bin/bash

apt update
apt install nginx -y
rm -rf /var/lib/apt/lists/*