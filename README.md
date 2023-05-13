# **django-graphql-learning**

# ***Context***
As part of our internship, we are assigned to a project spearheaded by our supervisor/s. In this project, we are given a task to learn GraphQL and Graphene. 

To prevent experiencing an excruiciating journey, I decided to go back to tutorial hell - speedrun mode, and this is a great opportunity for me to learn GraphQL, a part of the technologies that I want to learn in 2023.

# **About this Repo**
I will attempt to recreate the [library/bookstore app]((https://github.com/louispawaon/mugna-django-training)) that we followed throughout our training for Django step-by-step

## **Prerequsites**
- **Python** [^3.10](https://www.python.org/downloads/)
- **Poetry**
    ```
    curl -sSL https://install.python-poetry.org | python3 -
    poetry --version
    ```
- **Django** [^4.2.1]
    ```
    poetry add django
    pip install django
    ```
- **Graphene-Django**
  ```
  poetry add graphene-django
  pip install graphene-django
  ```
- **Requests**
  ```
  poetry add requests
  pip install requests
  ```
- **Black** (Optional)
  ```
  poetry add black
  pip install black
  ```

**Optional**: Run `poetry install` after installing Poetry to install the dependencies, if you plan to clone my repository

# ***Chores***
- [x] Initialize Models
  - [x] Books
  - [x] Publishers
  - [x] Authors
- [x] Necessary Migrations
- [x] Initialize Graphene-Django
  - [x] Necessary Graphene-Django Imports
  - [x] Necessary GraphQL Imports
  - [x] Necessary Graphene Imports
  - [x] Add `graphene_django` in `settings.py`
- [x] GraphQL Schema
  - [x] Initialize `schema.py`
  - [x] Create `DjangoObjectType` for the models
  - [x] Create `Query` 
  - [x] Create different mutations for CRUD Operations
    - [x] Add
      - [x] Publisher
      - [x] Book 
      - [x] Author
    - [x] Update
      - [x] Publisher
      - [x] Book 
      - [x] Author
    - [x] Delete
      - [x] Publisher
      - [x] Book 
      - [x] Author 
