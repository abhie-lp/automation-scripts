#!/bin/bash

echo $#

if [ $# -eq 0 ]; then
  echo Enter the email address for which the ssh key is to be created.
  exit
fi
ssh-keygen -t rsa -b 4096 -C $1
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
