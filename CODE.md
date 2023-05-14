<h1 align="center">How it works</h1>

I made a Flask developed website, that uses a MYSQL database. It connects, trough an API REST in the backend, to a HTML frontend, making the requests that the user needs using the routes configured on it. 

![back-front](https://i.imgur.com/DxFc1Sq.png)

# Backend

## Models and resources

Here i determine how the data is going to be stored and how the user is going to interact with it. With the resources and models of every aspect in the website, i made the requests from the frontend to the database.

* These are the models(the resources have the same name as the models):

![models-resources](https://i.imgur.com/5tk4AV7.png)

* Here is how i determine how the data is going to be stored in the database, regarding to the poems:

![img](https://i.imgur.com/Et8vMl6.png/img)

* From the resources, i import the models, also what i need to make the requests. I use the "flask_jwt_extended" to make the authentication of the user, and the "flask_restful" to make the requests.

![imports](https://i.imgur.com/lbfpbP3.png)

## API creation

* This is how i create the app, and the database. I also import the resources and add them to the api. 

![imgur](https://i.imgur.com/hY4XBzj.png)

## Autentication
* This is how i make the autentication of the user. I use the "flask_jwt_extended" to make the autentication, and the "flask_restful" to make the requests. In the routes, i make the login for the user
![auth](https://i.imgur.com/vmDqINJ.png)



