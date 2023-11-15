## Setup

### TPC-H Setup

Install docker, it will come with docker compose CLI.

If its the first time setting up, pull the postgres image using `docker compose create`.

To start the containers, run `docker compose start`, or start manually from the docker dashboard. To stop, run `docker compose stop`, or stop manually from the dashboard.

Once the container is running, the database can be initialised by running database.py.

Alternatively, the Database class can be imported to whicher script it is needed in, and created a Database object will initialise the DB as well.

If it is the first time initialising the DB, the process may take up to 5 minutes due to the large size of the data files.

### Dev Env Setup

#### List Python versions installed in your system

```
py --list

Mac
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

### Add newly install packages to requirements.txt

```
pip freeze >> requirements.txt
```

#### Deactivate Virtual Env

```
# Mac
source bin/deactivate

# Windows
deactive
```