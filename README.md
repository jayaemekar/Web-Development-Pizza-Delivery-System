# Cal Pizza Delivery System

### Team: Jayarani Emekar

The main objective of Cal Pizza Delivery web application is to help users place pizza order online and track order status online. 
This Web application should also provide option for users to track their orders and new users to register.

## List of Pages/Views:
##### Home page:
Home page should consist of four header navigation items Home, Menu, Orders, and About. 
##### New User Registration: 
Any new user should be able to go through registration page by clicking on Sign Up button from landing/home page.
##### Existing User Login: 
Existing user can login using their credentials.
##### Menu page: 
Menu should display list of menu items or pizzas available to order from the store.
##### Order Pizza Page: 
Post login/registration, users can place orders from this page.
##### Orders Page: 
Orders page should display list of user’s orders along with current in-progress orders.
##### Order Status Page: 
This page should have chat option using WebSocket to help users with their order status and request expedition if required.
##### About Page: 
This page is to display details about the store along with some social media profile details.


### Project Goals
1. User should be able to access the website using given URL.
2. User should be able to register as new user and place order using Menu options.
3. User should be able to login with existing credentials and place order using Menu options.
4. User should be able to use integrated chat service to track their orders or request for order status and expedition.
5. Integrated chat should be implemented using WebSocket and work as expected without any page refresh.
6. User should be able to navigate through review comments.
7. Admin user should be able to update order status in the back end.
### Project Stretch Goals
1. Mock payment API integration for online payments.
2. User can track their order status using Order Status page which can be implemented using WebSocket without page refresh.
3. User can update their review comments and see their review comments on About page and should be implemented using WebSocket.
4. Host this website on Google’s cloud
5. Login integration using social media like Google, Facebook, etc.
6. Menu customization from existing menu options.

### After cloning CalPizzaDelivery project to another machine:

01. Create a python environment in the working directory. It's better to user python version 3.9.6 for creating the environment. Activate the python environment.

		python3.9 -m venv env
		source env/bin/activate

02. Create a db instance into the new machine, using 'makemigrations'

		cd mysite/
		python manage.py makemigrations
		python manage.py migrate

    We need to create the superuser in order to use this project's django-admin-panel.
    
		python manage.py createsuperuser
	
        1. username: xyz
        2. email: xyz@gmail.com
        3. password: *******


03. Now run the django-server.

		python manage.py runserver 
