# How to install and run the project
* This project, that consists in a poems website, has its backend and frontend. I used somelibraries to make the project work, such as Flask, Flask-Login, etc. To run this project correctly, you have to intall them all in your virtual environment. 

## Installing requirements
* In both frontend and backend folders, you will find a file called requirements.txt. This file contains all the libraries you need to install in your virtual environment. But there is a "install.sh" file that will, first, create the environment and then install all the libraries you need. To run this file, you have to type in your terminal:
```bash
./install.sh
```
* This is what the file contains:
```bash
python3 -m venv .
source bin/activate
pip3 install -r requirements.txt
```
* The "pip install -r requierements,txt" command will install all the libraries you need to run the project.

## Running the project
### Env file configuration
* In both backend and forntend folder, you will find a file called ".env.example". This file contains the environment variables you need to run the project. You have to create a file called ".env" and copy the variables from the ".env.example" file. Then, you have to change the values of the variables to your own values. This is what the env example contains for the backend:
```python
export PORT = 8500
export DATABASE_PATH = 'path/absoluto'
export DATABASE_NAME = 'programacion.db'

#JWT configuration
export JWT_SECRET_KEY = 'estaesunaprueba'
export JWT_ACCESS_TOKEN_EXPIRES = 50000

#Config del mail
export MAIL_SERVER = 'smtp.gmail.com'
export MAIL_PORT = '587'
export MAIL_USE_TLS = 'False'
export MAIL_USERNAME = 'name@mail.com'
export MAIL_PASSWORD = 'pass'
#Mail FROM name
export FLASKY_MAIL_SENDER = 'App Name Admin <admin@appname.com>'
```

* In both frontend and backend folders, you will find a file called "boot.sh". This file will run the project. To run it, you have to type in your terminal:
```bash
./boot.sh
```
* Be sure that all the requirements are succesfully intalled before running this file. After doing the listed above, the project will be running in your localhost. For example, this is my boot.sh executed in a bash terminal, so you can access to the website from yout localhost, in my case, in port 3000.
![Imgur](https://i.imgur.com/CbnMVyO.png)

* Its important to know that the frontend and backend are running in different ports ,and at the same time, so the project works. The frontend is running in port 3000 and the backend is running in port 8500 on my pc, so you have to ensure that both ports you use on yours,are avaible. You can change this in the .env file.