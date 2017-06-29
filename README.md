# FlaskSampleProject

### This is a simple bookmarking web application. 
The application has been developed in Python with the Flask web framework and SqlAlchemy database framework.

### Architecture 
The application follows a MVT (model-template-view) pattern similar to the MVC (model-view-controller) design pattern.
* The templates contains the view HTML files built with the Jinja2 templating language for python.
* The views correspond to controllers that handle HTTP requests and issue responses. 
* The model is represented with the ORM (object-relational-mapper), SQLAlchemy and persisted in a SQLite file. 

### Modular Application with Blueprints 

The application uses Flask and its concept of blueprints for making its components.

These blueprints define how to construct or extend the application.

The application has a blueprint for the 3 main modules: 
* auth
  * Authentication functionality with views (i.e. controller actions) and forms (login, signup) 
* bookmarks
  * Bookmark functionality with bookmark views (i.e. controller actions) and forms (add, edit, delete etc)
* main 
  * Index page and error handler views (i.e. controllers actions) 
  
The blueprints are registered in the application in the main '__init__' python file in an app factory function (i.e. 'create_app'). 

### How to run the application

Use the manage.py script with the "runserver" command to run the application.
Note: use the migrations and database commands to setup the database (init command).
The config.py file contains configurations for different environments (production, development). 


