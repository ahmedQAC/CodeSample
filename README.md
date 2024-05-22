# Footballplanner REST API

The Footballplanner REST API is designed to allow users to create accounts and manage football sessions. Users can register using their Google account or email, create and update sessions, and view sessions they have created or joined.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)

## Requirements

- Python 3.12+

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/ahmedQAC/CodeSample.git
    cd CodeSample
    ```

2. **Create a virtual environment:**

    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - On Windows:

      ```sh
      venv\Scripts\activate
      ```

    - On macOS and Linux:

      ```sh
      source venv/bin/activate
      ```

4. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

5. **Create a .env file:**

    Create a `.env` file in the root directory of the project with the following variables:

    ```env
    SECRET_KEY=your_secret_key
    google_client_id=your_google_client_id
    google_secret=your_google_secret
    ```

    Replace `your_secret_key`, `your_google_client_id`, and `your_google_secret` with your actual values. The `SECRET_KEY` is used for cryptographic signing and should be a random string of characters. The `google_client_id` and `google_secret` are obtained from the Google Developers Console for OAuth authentication.

6. **Apply migrations:**

    ```sh
    python manage.py migrate
    ```

7. **Create a superuser (optional but recommended):**

    ```sh
    python manage.py createsuperuser
    ```

8. **Run the development server:**

    ```sh
    python manage.py runserver
    ```

## Usage

### Running the Server

Start the development server by running:

```sh
python manage.py runserver
```

### Accessing the server

The API will be available at http://127.0.0.1:8000/

## API Endpoints

Here is a list of the available API endpoints:

- **GET** `/admin/` - Django administration page
- **POST** `/api/users/` - Register a new user using email. (Requires: `username`, `email`, `password1`, `password2`)
- **POST** `/api/football/` - Create football session (Authentication Required)
- **PUT/PATCH** `/api/football/update/<int:pk>/` - Update football session specifying 'pk' (primary key) (Authentication Required)
- **POST** `/api/football/<int:pk>/` - Cancel football session specifying 'pk' (Authentication Required)
- **GET** `/api/football/hosted/` - View all hosted sessions (Authentication Required)
- **GET** `/api/football/all/` - View all hosted and joined sessions (Authentication Required)
- **GET** `/api/football/view/<int:pk>/` - View single session specifying 'pk' (Authentication Required)