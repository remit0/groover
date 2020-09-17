# Groover technical test

This test was made with django because of my past experiences and because it is the easiest way to address the challenge.
Indeed, django comes with a powerful ORM, serializers, ...
<br>
This code is not truly production ready as they are no tests, logs and no CI/CD tools provided.
<br>
<br>
I could not implement a few things with the time I had at my disposal, here I will discuss these points:
- I did not fully understand the pipeline of asking the user for the permission to access its spotify. Basically, to get the authorization code, you will have to manually click on the url given by `SpotifyAuth().getAuth()`. Then your browser should open and you should fill your account credentials. As a result, I only have to store one token for this account (rather than a token per user -- as I have not made use of an user database on this project). That seems a bit odd... I should have had linked this token to a registered user of this api and linked its spotify token to it.
- The way of handling spotify tokens is probably not perfect. I think there should probably be some django utility to handle third-party authentication.
- Http errors are not handled for authentication.
- The way albums and artists are persisted is suboptimal: when adding new instances, we perform an update of the database, regardless of if the instance already exists. While this works for our purpose, I believe it would be more efficient to check if the instance exists so that an update is not needed.
- I did  not know what specific information the user should retrieve from the artists database. I just returned the name, as an example, adding information is not complicated but time consuming. (manually parsing dicts and creating field in the model, or making a request to the artist api to add extra information then parsing dicts...)

# Setup
A few words about how you can run the project at home: 
- you will need to install the requirements
- you will need a `.env` at the root of this project with the secrets in it
- you will need to setup a postresql database and fill the secrets of the `.env` file with the name of the dabase, the user, login and password
- lastly, it seems that spotify only accepts to send requests to the port 5000, so you will have to run `python manage.py runserver localhost:5000` to launch the server

# Final words
If you have any question about the code, feel free to email me at remi-rosenthal@hotmail.fr, I will answer as soon as possible.