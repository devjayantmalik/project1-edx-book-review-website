# Project 1

Web Programming with Python and JavaScript

## Files and Their content

| File Name | Purpose | Description |
| ---------- | -------- | ----------- |
| app.py    | Contains Flask application | The app.py has seperate routes into multiple sections with the help of comments. The main sections are: Helper Functions, Logged In Routes, Api and Goodreads Routes, Authentication Routes
| import.py | Contains python code to import csv to database | Contains use of csv module and few lists and generator expressions. That helped to upload the data to database. The file also contains sqlalchemy module in order to execute database queries.
| books.csv | books and author data | The file was provided in the project 1 default template zip folder.
| Procfile | Setup App for heroku | The file helps to host the application on heroku.
| requirements.txt | The file contains list of all dependency required to run the project. The file was generated using pip freeze > requirements.txt
| templates/ | Contains html template files | The directory contains layout and other html files used to present the information to the user.

## App.js Helper Functions

I decided to distribute the code in functions to make it easy to organise. The code is still not properly organised, because it is all written in a single file.

Helper functions just execute the query and returns the data which is then used by the main application functions responsible for handling routes.

## App.js Logged In routes

The routes that will serve the content to logged in users only.

There are two different tasks such are signup and login that are not implemented in this section.

## App.js Api and Good Reads Routes

The section contains a function which just fetches information from goodreads api and returns it as json. This function is a helper function for api and other application routes.

The second function servers as an api route that is responsible for sending data to user.

## App.js Authentication Routes

The routes are login and signup, which allows a user to create a new account and login using the existing account.

For the simplicity the passwords are not encrypted before storing in the database.

## Video URL
The video is available on youtube, explaining all the functionality of the application. My videos are usually longer than 5 to 10 minutes, because i don't have editing skills. The video URL is [https://youtu.be/-irF01kCQ8c](https://youtu.be/-irF01kCQ8c)


## Thanks

I have tried to complete all the requirements specified by the Project 1. 

Happy Coding, and Thanks from Jayant Malik.


