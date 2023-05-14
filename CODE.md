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

## Autentication y security
* This is how i make the autentication of the user. In the routes, i make the login.
![auth](https://i.imgur.com/vmDqINJ.png)
![auth](https://images-ext-2.discordapp.net/external/qxbm7WSLQRLKfO7iH_V3Xd9qq8eSL4mHogmGNUYYAU4/https/i.imgur.com/MfdolGy.png)

* This is how i make the security of the user in the models. In the routes, i create the token verification.
![token](https://images-ext-1.discordapp.net/external/OKCeq265rVtkb_pIk04bJnW3m3BGWGJQpXjHwz09i5s/https/i.imgur.com/JXBCNts.png)

## Email
* I send and email whe any of his poems is rated. I use the "flask_mail" to send the email.
![email](https://images-ext-2.discordapp.net/external/jJMGDzxOrwGJieGuWb6hNW1lRh8iGlvvkBKEmgL_xEg/https/i.imgur.com/Aq1W0pF.png)

* This is the format it has:
![email_send](https://images-ext-2.discordapp.net/external/5WnEqYRtRHynaE-NpK-giJPgj3iTRzl8LDpK3YQQd-o/https/i.imgur.com/oAjF23Q.png?width=960&height=201)


# Frontend
* This is the main structure of my frontend:
![front-main](https://i.imgur.com/qsJvTdD.png)

## App
* This is the main app, where i register the routes.
![Imgur](https://i.imgur.com/4IIZQAa.png)

## Routes
* In the routes, i make the requests to the backend, and render the templates. For example, this is the route that renders the main page, for a user that is not logged in:
![Imgur](https://i.imgur.com/AtdxiJy.png)
![Imgur](https://i.imgur.com/Ox8mUct.png)

### Functions
* I made a group of functions that i use in the routes, to make the code more readable. For example, this is the function that i use to get the poems from the database, using the user id:
![Imgur](https://i.imgur.com/l9JNp66.png)

* There are a lots of functions like this one, because i need them to make the requests of everything to the database.

## Templates
* These are all the templates i use for my poems website:
![Imgur](https://i.imgur.com/MfJIjwh.png)

* I usea a Jinja2 template engine, using a "base.html" as the base of all the templates. That helps to all the other templates to be less repetitive, and to make a better code structure.
![Imgur](https://i.imgur.com/MFMsYkm.png)

* This is how i call the base template in the other templates:
![Imgur](https://i.imgur.com/bZfveEp.png)

## Static
* This is the static folder, where i store all the static files of the website:
![Imgur](https://i.imgur.com/A2qyWKu.png)

* This are the css file i use to style the website:
![Imgur](https://i.imgur.com/A2qyWKu.png)