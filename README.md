# Django Polls App

[![Python Version](https://img.shields.io/badge/python-3.8.2-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-3.0.7-brightgreen.svg)](https://djangoproject.com)

This is a simple polls app which has taken from django's [official documentation](https://docs.djangoproject.com/en/3.0/intro/tutorial01/).

## Running the Project Locally

First, clone the repository to your local machine:

```bash
git clone https://github.com/shaonsust/poll-app.git
```

Install the requirements:

```bash
pip install -r requirements.txt
```

Apply the migrations:

```bash
python manage.py migrate
```

Finally, run the development server:

```bash
python manage.py runserver
```

The project will be available at **127.0.0.1:8000/polls/index**.

## License

The source code is free. This has taken from django's [official documentation page](https://docs.djangoproject.com/en/3.0/intro/tutorial01/).
