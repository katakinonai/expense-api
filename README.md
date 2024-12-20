# Expense API
[Project on roadmap.sh](https://roadmap.sh/projects/expense-tracker-api)

Build an API for an expense tracker application. This API should allow users to create, read, update, and delete expenses. Users should be able to sign up and log in to the application. Each user should have their own set of expenses.

## Start
To start the project, you need to clone the repository and install the dependencies.

```sh
git clone
cd expense-api
pip install -r build/requirements.txt
```

To run the project, you need to run the following command:

```sh
make serve
```

## Expense Tracker API
### Features

Here are the features that you should implement in your Expense Tracker API:

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

### Constraints

You can use any programming language and framework of your choice. You can use a database of your choice to store the data. You can use any ORM or database library to interact with the database.

Here are some constraints that you should follow:

    - You’ll be using JWT (JSON Web Token) to protect the endpoints and to identify the requester.
    - For the different expense categories, you can use the following list (feel free to decide how to implement this as part of your data model):
        * Groceries
        * Leisure
        * Electronics
        * Utilities
        * Clothing
        * Health
        * Others

This is the last “beginner” project in the backend roadmap. If you have completed all the projects in the backend roadmap, you should have a good understanding of how to build a backend application. You can now move on to the “intermediate” projects in the backend roadmap.

