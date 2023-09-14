# Setting Up SQLAlchemy and Alembic Migration in FastAPI Application

## **Part 1: Setting Up SQLAlchemy in FastAPI Application** 

This README guide will help you set up and understand the structure of your FastAPI project. Follow the steps below to get started:

### Step 1: Install Required Libraries

In your project's `requirements.txt` file, include the following libraries:

```plaintext
fastapi[all]
sqlalchemy
uvicorn  # Used to run the gateway server
alembic  # Used for Alembic migration
psycopg2-binary  # Driver for connecting to PostgreSQL
```

### Step 2: Create the `main.py` File for Your FastAPI Application

In the `main.py` file, you will write your FastAPI application with basic endpoints. Additionally, you'll create a function called `get_db()` to retrieve a database connection from the SQLAlchemy connection pool.

```python
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from models import User, SessionLocal

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Your endpoint implementation here
```

### Step 3: Define Database Models and Schemas

Create the models.py and schemas.py files to define your database models and request/response schemas using Pydantic.

In `models.py` file: 

```python
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserModel(Base):
    # Define your User model here

class TenantModel(Base):
    # Define your Tenant model here
```

**`Notice`**: All model classes must be inherited from Base class of SQLAlchemy to define database models!

<br>

In `schemas.py` file: 

```python
from pydantic import BaseModel

class User(BaseModel):
    # Define your User schema here

class UserCreate(BaseModel):
    # Define your UserCreate schema here

class Tenant(BaseModel):
    # Define your Tenant schema here

class TenantCreate(BaseModel):
    # Define your TenantCreate schema here

```

### Step 4: Set Up Database Connection
In the database.py file, configure the connection to your desired database, whether it's SQLite or PostgreSQL.

```python
Copy code
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Setup database connection for SQLite database
# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Setup database connection to PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost:5432/database_name"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)
```

This code above has tried to: 
- To setup connection to our expected database: 
    - With an SQLite database: When you run a FastAPI application, it will automatically create a database file named `test.db`.
    - With a PostgreSQL database: You need to create a database in advance (using the PgAdmin Tool) and then provide all the credential information in this format: `SQLALCHEMY_DATABASE_URL = 'postgresql://username:password@localhost:5432/database_name`
- And then using Base module (imported from `models.py` file) to create all defined tables in the database.

<br>

### Step 5: Run Your FastAPI Application
To start your FastAPI application and create all the necessary database tables, run the following command:

```
    python3 main.py
```

This command will launch your FastAPI application and automatically generate the required database tables.

That's it! You have successfully set up your FastAPI project. Feel free to expand and customize it to suit your specific needs.

**`Notice`**:  
- This basic guide is designed to help you understand the core concepts of integrating SQLAlchemy with FastAPI.
- In larger systems, it's recommended to separate the `get_db()` function into an own file and organize your models.py file into a folder with individual files to define each database table (with its fields).

<br>

---

## **Part 2: Continue integrating Alembic Migration with SQLAlchemy in FastAPI Application** 

## Purpose
The Alembic library in Python is a tool that helps manage database schema migrations during the development of a product. Specifically, during the development of a database, at each version, you may need to update certain fields in the database (add/modify/delete fields or add/modify/delete tables). As development progresses, the number of these operations increases, and simply updating the database model in code has limitations, such as only storing the latest model schema. This makes it impossible to track changes in older versions of the database, making it challenging to revert to a previous state.

As a result, there is a need for a tool or library to manage all changes to the database schema during development. This involves creating a set of migration files to store each change to the database schema. This way, you can easily revert the database schema to a specific point in the past when needed. This makes managing database schema changes in software development much more convenient.

In Python, the Alembic library is used to manage the database migration process.

## Steps to Integrate Alembic with SQLAlchemy and FastAPI Application

### Step 1: Install the Alembic Library
You can install the Alembic library using pip:

```bash
pip install alembic
```

Alternatively, add the `alembic` library to your requirements.txt file and run:

```bash
pip install -r requirements.txt
```
### Step 2: Comment or Remove the SQLAlchemy Database Table Creation
Comment or remove the code responsible for creating all the tables in the database using SQLAlchemy. You will now manage all database schemas and migrations using the Alembic library.

```python
# # Create tables
# Base.metadata.create_all(bind=engine)
```

### Step 3: Create and Set Up the 'alembic' Directory in Your Project

Run the following command:

```
alembic init alembic
```

After running this command, the following will be created:

- `alembic.ini`: Contains configurations for Alembic, such as the database URL and logging settings.
- `alembic` directory: Manages the entire migration process, including:
  + `versions`: Stores all migration files that track changes to the database schema over time.
  + `env.py`: Loads all Alembic configurations from the alembic.ini file into the 'config' object in this file. It points to the file that defines all the database models and sets up the database connection URL. This setup allows Alembic to detect changes in the current database schema by comparing it to the most up-to-date schema defined in your code. Alembic then creates a migration file to record changes from the most recent version to the current version.


### Step 4: Configure Alembic to Point to the File Defining Database Models and the Database URL
Let Alembic know the file defining your database models, you need to edit the `alembic/env.py` file and import the module that defines your models as follows:

```python
from models import Base
target_metadata = Base.metadata
```

Then, let Alembic know the database URL, please add the following line to the alembic.ini file:

```bash
sqlalchemy.url = postgresql://username:password@localhost:5432/database_name
```

- Replace the URL with your database's connection details. This URL is used by Alembic to connect to the database when running migrations.

<br>

`Advance Notice`: 
- If you want to set the database URL using an environment variable for security reasons, you can do the following:

    - In the alembic.ini file, leave the URL blank:

        ```bash
        sqlalchemy.url =
        ```

    - In the alembic/env.py file, add the following line to retrieve the database URL from the environment variable:

        ```python
        config.set_main_option("sqlalchemy.url", os.environ["DATABASE_URL"])
        ```

    This command fetches the DATABASE_URL environment variable, which should be set securely in your server environment (or docker environment). It then sets this value as the `sqlalchemy.url` parameter in Alembic.

### Step 5: Running Migrations
To create the initial migration, run the following command:

```bash
alembic revision --autogenerate -m "Initial Migration"
```

- This command automatically generates a migration file that contains all the commands necessary to create all the tables defined in your models.py file. For example, the file may look like this: '78caea8126e5_initial_migration.py'.


To apply the initial migration and create all the tables in the database, run:

```bash
alembic upgrade head
```

- After running this command, your database will contain all the necessary tables, and an 'alembic_version' table will be created to track the current migration version. This table helps you easily determine which migration version is currently applied.

In the future, if you make changes to the database schema in your models.py file, you can generate a new migration file by running:

```bash
alembic revision --autogenerate -m "Your Next Migration"
```

You can then customize the script in the generated migration file. Once you're satisfied with the migration script, you can apply it to the database by running:

```bash
alembic upgrade head
```

This allows you to easily manage and apply database schema changes over time.

### Step 6: Upgrading or Downgrading to a Specific Migration Version
Use the following commands to upgrade or downgrade your database schema to a specific migration version:

**Upgrade to a specific revision:**
```bash
alembic upgrade <revision_id>
```

For example:
```bash
alembic upgrade 22222222
```

- This command upgrades the database schema from a previous revision to the specified revision. It runs the 'upgrade()' function in the migration file associated with the specified revision to apply the changes to the database schema.


**Downgrade to a specific revision:**
```bash
alembic downgrade <revision_id>
```
For example:

```bash
alembic downgrade 11111111
```
- This command downgrades the database schema from a newer revision to the specified revision.

**Upgrade to the latest revision:**
```bash
alembic upgrade head
```
- This command upgrades the database schema to the latest revision.

With these steps, you can effectively manage database schema migrations in your FastAPI application using Alembic and SQLAlchemy.

Feel free to modify or add any additional details as needed for your README.md file.