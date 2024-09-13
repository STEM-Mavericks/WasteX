#!/bin/bash
while true; do
  git pull --rebase        # Pull the latest changes from the remote branch
  git add .
  git commit -m "Auto Commit"
  git push
  sleep 300
done
