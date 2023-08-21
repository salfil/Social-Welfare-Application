## Social Welfare helper application

This is a django web application where social workers and staff members can connect with their users, post programmes and for users to gain directions to appointments booked and access a range of programmes and support. 

file types submitted include: python files, javascript files, CSS files, HTML files, images, sqlite file

Visual Studio Code was used to write and edit the code. Executable file not inclded as it is a web app. Steps to run the code are given below. 

## Installation
- Must have django installed in your command prompt. 
- Must have python installed
- CSS, JavaScript, Bootstrap and HTML required (latest version)
- Dependancies: requests, random, datetime. install by writing "pip install" then write the dependancy. 

## Running code 
Run code by 
- Decompressing/extracting the zip file, 
- Navigate to the directory of the code on your command prompt ( by writing cd to the development directory in the command prompt). 
- write "pip install" for each of the dependancies listed above. 
- In the command prompt then write "python manage.py makmigrations"
- Then write "python manage.py migrate"
- In the command prompt then type "python manage.py runserver". You must be on the same directory as the manage.py file for this command to work. 

## If above does not work then follow the steps below. You would have to create a new project then move the files downloaded onto this project. 

- write on command prompt "django-admin startproject fyp"
- write on command prompt "python manage.py startapp finalyearproject"
- write on command prompt "python manage.py startapp users". 
- copy and paste all the files in the fyp folder downloaded into the fyp folder just created (this should have  the settings.py file in it.)
- copy and paste all the files in the finalyearproject folder downloaded into the finalyearproject folder just created
- copy and paste all the files in the users folder downloaded into the users folder created
- copy and paste all other files/folders from the downloads onto the project just created. (especially the settings.py file)
- use "pip install" to install the mentioned dependancies such as "pip install requests"
- write on command prompt "python manage.py makemigrations" (if not working try to include the app name either users or finalyearproject)
- write on command prompt "python manage.py migrate"
- write "python manage.py runserver"

## Admin
- write on the code python manage.py createsuperuser to create an admin user where you will be asked for a username and password
- run the code and write http://127.0.0.1:8000/admin on the browser where you will be asked to login
- once logged in you should see all the models. 

## Make sure to have a valid google API key to faciliate the directions functionality. I used my own key so follow the steps below to generate your own API key. 

    - create a google account on the google maps platform
    - create a project and enable the places API, Maps Javascript API, Directions API, Distance Matrix API and the Geocoding API . 
    - go on credentials where you will have access to your key.  
    - go onto the settings file and insert the google api key in the following way:  GOOGLE_API_KEY= "XXX"


## If you have any questions feel free to email me at ec19143@qmul.ac.uk
