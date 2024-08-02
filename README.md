# Flask RESTful API

## Overview

This project is a simple RESTful API built with Flask, SQLAlchemy, and Flask-Restx. It includes user registration, login, password reset, and basic user management functionalities. The API uses JWT for authentication.

## Features

- User registration
- User login
- Password reset functionality
- User management (update, delete, list users)
- Admin-specific endpoints
- JWT-based authentication
- OpenAPI (Swagger) documentation

## Requirements

- Python 3.6+
- PostgreSQL
- Virtualenv

## Setup Instructions

### Clone the Repository

```sh
git clone [<repository_url>](https://github.com/miraz-ezaz/Flask-Assignment.git)
cd Flask-Assignment
```

### Create and Activate Virtual Environment

```sh
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Install Required Packages

```sh
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the root of your project and add the following environment variables:

```env
DATABASE_URI=postgresql://your_username:your_password@localhost/your_db_name
JWT_SECRET_KEY=your_jwt_secret_key
SECRET_KEY=your_secret_key
```

### Run Migrations

```sh
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

### Run the Flask Application

```sh
flask run
```

The application will be available at `http://localhost:5000/`.

## API Documentation

The API documentation is available at `http://localhost:5000/` using Swagger UI.

### Endpoints

#### User Registration

- **Endpoint**: `POST /api/register`
- **Description**: Registers a new user.
- **Request Body**:

  ```json
  {
    "username": "your_username",
    "first_name": "First",
    "last_name": "Last",
    "email": "email@example.com",
    "password": "your_password"
  }
  ```

- **Response**:

  ```json
  {
    "message": "User registered successfully"
  }
  ```

#### User Login

- **Endpoint**: `POST /api/login`
- **Description**: Logs in a user and returns a JWT token.
- **Request Body**:

  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```

- **Response**:

  ```json
  {
    "access_token": "your_jwt_access_token"
  }
  ```

#### List Users

- **Endpoint**: `GET /api/users`
- **Description**: Lists all users (Requires JWT).
- **Response**:

  ```json
  [
    {
      "id": 1,
      "username": "username1",
      "first_name": "First",
      "last_name": "Last",
      "email": "email@example.com",
      "role": "User",
      "create_date": "2022-01-01T00:00:00",
      "update_date": "2022-01-01T00:00:00",
      "active": true
    },
    ...
  ]
  ```

#### Get User by Username

- **Endpoint**: `GET /api/user/<string:username>`
- **Description**: Retrieves user details by username (Requires JWT).
- **Response**:

  ```json
  {
    "id": 1,
    "username": "username1",
    "first_name": "First",
    "last_name": "Last",
    "email": "email@example.com",
    "role": "User",
    "create_date": "2022-01-01T00:00:00",
    "update_date": "2022-01-01T00:00:00",
    "active": true
  }
  ```

#### Update User by Username

- **Endpoint**: `PUT /api/user/<string:username>`
- **Description**: Updates user details by username (Requires JWT).
- **Request Body**:

  ```json
  {
    "first_name": "NewFirstName",
    "last_name": "NewLastName",
    "email": "newemail@example.com",
    "active": false
  }
  ```

- **Response**:

  ```json
  {
    "message": "User updated successfully"
  }
  ```

#### Delete User by Username

- **Endpoint**: `DELETE /api/user/<string:username>`
- **Description**: Deletes user by username (Requires JWT).
- **Response**:

  ```json
  {
    "message": "User deleted successfully"
  }
  ```

#### Admin List Users

- **Endpoint**: `GET /api/admin/users`
- **Description**: Lists all users (Admin only, Requires JWT).
- **Response**:

  ```json
  [
    {
      "id": 1,
      "username": "username1",
      "first_name": "First",
      "last_name": "Last",
      "email": "email@example.com",
      "role": "User",
      "create_date": "2022-01-01T00:00:00",
      "update_date": "2022-01-01T00:00:00",
      "active": true
    },
    ...
  ]
  ```

#### Request Password Reset

- **Endpoint**: `POST /api/reset_password_request`
- **Description**: Requests a password reset token.
- **Request Body**:

  ```json
  {
    "email": "email@example.com"
  }
  ```

- **Response**:

  ```json
  {
    "message": "If your email is registered, you will receive a password reset token shortly."
  }
  ```

- **Note**: The token will be printed on the console for simplicity.

#### Reset Password

- **Endpoint**: `POST /api/reset_password/<token>`
- **Description**: Resets the password using the reset token.
- **Request Body**:

  ```json
  {
    "password": "new_password"
  }
  ```

- **Response**:

  ```json
  {
    "message": "Your password has been reset successfully."
  }
  ```

### Using JWT Token in Swagger UI

1. **Login and Get Token**: First, use the `/api/login` endpoint to log in and get your JWT token.
    - **Endpoint**: `POST /api/login`
    - **Request Body**:

    ```json
    {
        "username": "your_username",
        "password": "your_password"
    }
    ```

    - **Response**:

    ```json
    {
        "access_token": "your_jwt_access_token"
    }
    ```

2. **Authorize Requests**: 
    - Copy the `access_token` from the response.
    - Open the Swagger UI at `http://localhost:5000/`.
    - Click the "Authorize" button (usually a green lock icon) at the top right of the Swagger UI.
    - In the "Value" field, enter `Bearer your_jwt_access_token`.
    - Click "Authorize" and then "Close".

Now, the token will be included in the headers of your requests, and you can access the secured endpoints.

## Troubleshooting

### Flask Not Found

If you encounter an issue where Flask is not found after running `pip install -r requirements.txt`, follow these steps:

1. **Create and Activate Virtual Environment**:

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

2. **Install Required Packages**:

    Ensure you're in the root directory of your project (where `requirements.txt` is located) and run:

    ```sh
    pip install -r requirements.txt
    ```

3. **Verify Flask Installation**:

    ```sh
    pip show Flask
    ```

    This command should display information about the Flask package if it is installed correctly.

4. **Manually Install Flask**:

    If Flask is still not found, you can manually install Flask to ensure it is available:

    ```sh
    pip install Flask
    ```
