## Python FastAPI - Async HTTP Server 

#### This application was created to show in a list of projects that I've made for my portfolio website. It is an example model but can be used for production.
Details:<br/>
CRUD operations to a MongoDB Database using ODM classes and JSON. <br/>
Firebase for user authentication and cache with Redis.

### App structure:
```commandline
auth
       firebase.py      # User authentication
           
cache
       base.py          # Base cache
       product.py       # Product cache, inherits from BaseCache
       .                # Other cache classes...

common
       config.py        # App configuration (singleton)
       constants.py     # Environment variables

model                # Each class is a Mongodb collection
       product.py

router
       api.py           # Base router
       product.py

schema
       base.py          # Base transaction schema
       product.py
```

### Deploy
All the project configuration and dependencies are specified in the **DOCKERFILE** and **docker-compose.yml** file.<br/>

**App dependencies:**<br/>
**Docker:** you need one mongodb and one redis instance running and connected to the same docker network as this app<br/>
**Firebase:** .json configuration file of your firebase project to manage user authentication, this API validates users from a firebase bearer token inside the "Authentication" request header.


**Run:**
```
docker compose build
docker compose up -d
```
Note: make sure to create an .env file with your environment variables, 
the names are specified under the "environment" key in the **docker-compose.yml** file.
