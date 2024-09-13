#!/bin/bash
while true; do
  # Stash any unstaged changes
  git stash -u
  
  # Pull the latest changes with rebase
  git pull --rebase
  
  # Apply stashed changes back
  git stash pop
  
  # Stage all changes
  git add .
  
  # Commit the changes
  git commit -m "Auto Commit"
  
  # Push the changes to the remote repository
  git push
  
  # Wait for 5 minutes before the next iteration
  sleep 300
done
