#!/bin/bash
while true; do
  git stash -u
  git pull --rebase
  git stash pop
  git add .
  git commit -m "Auto Commit"
  git push
  sleep 100
done
