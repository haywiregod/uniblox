# Django E-commerce
This project is a basic e-commerce platform built with Django and Django Rest Framework.

## Features
- User authentication and authorization
- Cart management
- Order Placement
- Coupon Application

## Installation
- Clone the repository
- Create and activate a virtual environment
- Install the dependencies with `pip install -r requirements.txt`
- Run the migrations with `python manage.py migrate`
- Run the server with `python manage.py runserver`

## Usage
- Database with pre-populated data is included in the repository
- Use the API endpoints to interact with the platform
- On signup, you'll get a token that you can use to make authenticated requests. Set `Auhorization: Bearer <token>` in the headers of your requests

## API Endpoints
[Use Postman](https://www.postman.com/blue-comet-496858/workspace/uniblox/collection/14929837-596dbc60-508d-4b3d-aac4-468d724bcbb9?action=share&creator=14929837&active-environment=14929837-525631eb-46e4-405a-aa08-66c31d9f7b65)

## Technologies Used
- Django 5.1.7
- Django Rest Framework 3.13.1
- Python 3.10.11
- SQLite 3.37.0

