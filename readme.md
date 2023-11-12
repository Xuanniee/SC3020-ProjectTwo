## Setup

### TPC-H Setup

Install docker, it will come with docker compose CLI.

If its the first time setting up, pull the postgres image using `docker compose create`.

To start the containers, run `docker compose start`, or start manually from the docker dashboard. To stop, run `docker compose stop`, or stop manually from the dashboard.

### Dev Env Setup

#### List Python versions installed in your system

```
py --list
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