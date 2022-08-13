# Django Register System

User registration and login system project made with Python language using Django Framework.

## About

This project is part of my Django study. It is a register system where a user can create an account, log in and logout. [Django](https://www.djangoproject.com/) is a framework written in Python for web development.

## Status

The project development is completed. But in the future it can be added new features or fixes.

## Get started

The project is not deployed yet. For now, the only way to run it is locally.

- First, clone the project with `git clone` or download it in `.zip` format.
- Run `pip install -r requirements` in the shell at the project folder to install all the packages needed.
- Change the name of the file `.env-example` to `.env` and change the variables values if needed.
- Run `python manage.py migrate` to create the tables in the database.
- If you want to access the admin page, run `python manage.py createsuperuser` in the shell to create a superuser to access it.
- Run `python manage.py collectstatic` in the shell to collect all the static files.
- Run `python manage.py runserver` in the shell and access the page http://localhost:8000 in your browser and you will see the project running.

## Technologies

### Frontend

The focus of the project is the backend, so the frontend was built simply with [Bootstrap](https://getbootstrap.com/). The pages are:

- ***<u>Index:</u>*** the home page of the project. The page content it will be different if the user is authenticated or not.
- ***<u>Sign up:</u>*** page with the user creation form. The user has to fill the fields to create an account.
- ***<u>Login:</u>*** page with login form for users already created.

### Backend

All the backend was written in Python with Django. The user creation and authentication was made using Django built-in tools.

- **<u>*User Model:*</u>** Django already has a complete [User Model](https://docs.djangoproject.com/en/4.1/ref/contrib/auth/#django.contrib.auth.models.User) with several resources. Here, it was used this model, but it was customized to make the e-mail field the username field.
- ***<u>Forms:</u>*** it was used the [Django Forms](https://docs.djangoproject.com/en/4.1/topics/forms/) to build two forms:
  - *<u>Sign up form:</u>* a model form to create the user with the fields of the user model and an extra field to confirm the password. There is a `__init__` method to set all form fields with the CSS class from Bootstrap, and there are e-mail and password validation methods.
  - *<u>Login form:</u>* a form with only e-mail and password fields. There also is the same `__init__` method.
- ***<u>Views:</u>*** there are four [Django Views](https://docs.djangoproject.com/en/4.1/topics/http/views/) that render the pages:
  - <u>*Index view:*</u> a view for render the home page.
  - *<u>Sign up view:</u>* a view for render the sign up form and checks if the form data is correct to save it in the database or not. It is responsible for encrypt the user password and make the user user authentication after the creation so it will redirect him to the home page.
  - *<u>Login view:</u>* a view for render the login form that checks if the user exists in the database and makes the authentication.
  - *<u>Logout view:</u>* a view that delete all user data from the session so the user can logout of the system.
- ***<u>Tests:</u>*** the project is covered with unit tests made with `unittest`.

### Database

The database used is [PostgreSQL](https://www.postgresql.org/). You have to change the database configuration in the `.env` file for the database in your system. Or you can change the settings for the standard Django SQLite if you don't have PostgreSQL installed. Just change the database configuration in `simplelogin/settings.py`  for:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

