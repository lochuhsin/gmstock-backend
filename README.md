# gmstock-backend


### Using poetry as default packag management

If poetry isn't installed,
* pip install poetry ( remenber to install global)

Adding package to poetry lock
* poetry add [package name]

Activate virtual environment
* poetry shell

Startup
* docker-compose -d --build

Add migration

1. go into docker container
2. modify script.py.mako
3. alembic revision -m "<purpose>"
4. alembic upgrade head
