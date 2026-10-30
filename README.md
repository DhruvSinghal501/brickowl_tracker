🧱 BrickOwl LEGO Star Wars Tracker
An automated tracking tool that scrapes catalog listings, prices, and availability for LEGO Star Wars items from BrickOwl and maintains an up-to-date JSON dataset.

🚀 Features
Automated Scraping: Fetches live LEGO Star Wars data from BrickOwl (tracker.py).

Data Persistence: Outputs structured tracking data directly to brickowl_starwars_tracker.json.

One-Click Sync: Includes a Windows Batch automation script (sync.bat) to update data and push changes directly to GitHub in a single step.

📁 Repository Structure
app.py: Web application / UI entry point

tracker.py: Scraper logic for BrickOwl data

brickowl_starwars_tracker.json: Generated dataset storing tracker results

sync.bat: Automation script for execution and GitHub syncing

README.md: Project documentation

🛠️ Usage
Running the Tracker
To update the local dataset and automatically sync the results to GitHub, run the batch script in terminal or double-click it:

sync.bat

Or execute the Python scraper manually:

python tracker.py

🧰 Tech Stack
Language: Python

Environment: VS Code / Windows PowerShell

Version Control: Git & GitHub