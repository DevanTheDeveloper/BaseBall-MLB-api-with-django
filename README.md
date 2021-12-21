####
BASEBALL DEMO - 1st Assignment
####

Setup environment:

install latest version of python & pip 

pip install -r requirements.txt

manage.py runserver

Navigate to: http://127.0.0.1:8000/mlb/


####
Test User Account (*Optional, only enables the ability to upload/download csv's, site is fully navigational without logging in)
####

Username: 'Demo

Password: 'Testing1!'


####
Features
####

- 3 views for data collected from MLB API provided in project details: AllTeams, Team/Roster, PlayerProfile,

- Two interactive plotly charts generated from a sample baseball csv stats that were uploaded to database with details stored in sql. Also created upload/download report views. Accessible through Sidebar "Graphs" button.
 
- User authentication, basic profile page.

DATABASE - SQLITE3
