# APAD-Project

## Project1 - Description July 18, 2019
## 1 Project 1: Application Utilities in Python
The goal of the three course projects is to get towards building a finished "Web Application". The three project iterations will get us there incrementally 
- Project1: Develops the basic data model in SQL for storing out application’s data, followed by python utility functions to manipulate the data. 
- Project2: Deploys the application to the "cloud" (Googel App Engine’s appspot.com site) and present’s a web interface to the application. 
- Project3: Develop an Android app (written in Kotlin) to access the site.
This document will focus on the preliminaries to get you started. I will use an application called "PickupSport" as the context for explaining what your project must possess in terms of features. You may use this project or come up with your own.
The narrative: There are a lot of venues for pickup sports in Austin but there is no way to find out where there is one now (or in the future) that one can join. Enter PickupSport site that allows you to either start a new pickup sport event
or join one that somebody already started


### 1.1 1. Things of Interest
1. Users: These are people who use the application
2. Venues: These are the places where a pickup sport event may be planned
3. Events: These are the events that are currently in play
### 1.2 2. Business Rules
0. Admin manages the site and is able to do operations not permitted to a user
1. Users play in events
2. Venues are available in timeslots of 1-hr during contiguous operating time
3. A user can start an event at a particular venue at a specific timeslot by specifying a descrip-
tion and capacity
4. Events are at a venue for a timeslot and have a capacity
5. A user can join an event if there is room
### 1.3 3. Operations
Each of these are python functions you must write: 
1. Add a new user (admin only) -> Pei-Hsin
2. Add a new venue (admin only) -> Chetna
3. Start an event (user or admin on behalf of a user) -> Pei-Hsin
4. Display timeslot availability at a venue -> Chetna
5. Display all venues where a particular timeslot is available -> Chetna
6. List events at a venue given date/time -> Pei-Hsin
7. User joins an event -> Chetna
8. Remove an event (admin only) -> Pei-Hsin
9. checkAdmin -> Pei-Hsin
10. CalculateTimeslots -> Chetna
11. SingleVenueSingleTimeslotAvailability -> Chetna
