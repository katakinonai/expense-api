# Expense API
[Project on roadmap.sh](https://roadmap.sh/projects/expense-tracker-api)

Build an API for an expense tracker application. This API should allow users to create, read, update, and delete expenses. Users should be able to sign up and log in to the application. Each user should have their own set of expenses.

## Start
To start the project locally, you first need to clone the repository:

```sh
git clone https://github.com/katakinonai/expense-api.git
cd expense-api
```

### Docker

Instructions for running as a Docker container:

```sh
docker build -t expense_api:latest .
docker run -p 8000:8000 expense_api
```

App is now available at http://localhost:8000.

### Run locally

Create a Python virtual env and install dependencies:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r build/requirements.txt
```

To run the project, you need to run the following command:

```sh
make serve
```
App is now available at http://localhost:8000.

## Docs
To see the API documentation, you need to open the following link in your browser:

http://127.0.0.1:8000/docs

## Expense Tracker API
### Features

Here are the features that are implemented in Expense Tracker API:

    - Sign up as a new user.
    - Generate and validate JWTs for handling authentication and user session.
    - List and filter your past expenses. You can add the following filters:
        * Past week
        * Past month
        * Last 3 months
        * Custom (to specify a start and end date of your choosing).
    - Add a new expense
    - Remove existing expenses
    - Update existing expenses
