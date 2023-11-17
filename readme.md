### Generality

This project was made with generality in mind, therefore, a few assumptions are made:

* Postgres has been properly installed on the user's device
* The user's preferred database has been created
* All the tables in the database have been created, and they have been populated with data
* A postgres superuser with the appropriate credentials exists



However, to allow user's to use our app with minimal setup, we have provided the raw TPC-H data as well as initialisation of the database and data within the code as well.
* To use the built-in initialisation features, follow the instructions under `TPC-H setup`
Install docker, it will come with docker compose CLI.

## Setup

### Docker environment

To create an isolated postgresql instance, the following instructions can be followed to run postgresql in a docker container. However, the data must still be initialised by the user

* Install docker, it will come with docker compose CLI.
    + https://www.docker.com/products/docker-desktop/
* Once docker has been installed, open a terminal at the root folder and run the command `docker compose create`. This will pull the official postgresql image and create a user with both the username and password as "postgres"
* Once the image has been pulled, start the container using `docker compose start` from the terminal, or manually from the docker dashboard. To stop the container, use `docker compose stop`, or manually through the dashboard as well.
* Once the container is running, the next steps can be followed.

### Env Setup

#### List Python versions installed in your system

Windows
```
py --list
```
Mac
```
python --version
```

#### Specify a Python version that is 3.8 or higher. If unavailable, install it first then run the following command

```
py -3.8 -m venv venv
```

#### Activate Virtual Env

```
# Mac
source venv/bin/activate

# Windows
.\venv\scripts\activate
```

#### Install Packages

```
pip install -r requirements.txt
```

NOTE: If encountering issues with installing the `psycopg2` package, ensure that postgresql v16 is also installed directly on your machine, and run the following commands:
```
pip uninstall psycopg2
pip uninstall psycopg2-binary
pip install -r requirements.txt
```

### Running the app

NOTE: The Database connection parameters in project.py must be modified appropriately, else the app will fail to run.
```

#### Deactivate Virtual Env

```
# Mac
source bin/deactivate

# Windows
deactive
```