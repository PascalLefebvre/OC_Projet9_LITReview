# Openclassrooms - Project 9 : Develop a Web application using Django

    The LITReview web application is an MVP that allows a users community to ask and publish articles or books reviews.
	

## Installation


    - After cloning, change into the directory and type 'python -m venv env'.

    - Next, type 'source env/bin/activate' to enter in your virtual environment (to deactivate, type 'deactivate').

    - Type 'pip install -r requirements.txt' to install all the necessary packages.
    
    - To start the application, type 'python manage.py runserver'. The app should respond with an address you should be able to go to using your browser (http://127.0.0.1:8000 by default).


## Testing

    You can test the app by creating a new user from the app login page. To follow up existing users, you access to their username by the Django admin interface (see below).


## Management of the applicaton from the Django admin interface


    - From the app directory, type 'python manage.py createsuperuser' to create a superuser to manage the database.
    
    - To login to the Django admin site, open the /admin URL (e.g. http://127.0.0.1:8000/admin ) in your browser and enter your new superuser name and password. Then, you can access to the tables content.
    
    - See the database UML diagram ("UML_BD_schema.pdf")

