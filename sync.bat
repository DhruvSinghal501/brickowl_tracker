@echo off
cd /d "C:\Users\dhruv\Documents\brickowl_tracker"

echo Running BrickOwl Tracker...
python tracker.py

echo Syncing with GitHub...
git add .
git commit -m "Auto-update tracker data [skip ci]"
git push origin main

echo Sync complete!
pause