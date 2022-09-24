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


# streaming data format
"""
 dataformat
 {
  "_id":"ObjectId(""632dd03e1133651df91dbecc"")",
  "datetime":datetime.datetime(2022,9,20,0,0),
  "open":168.89999,
  "high":170.3,
  "low":166.10001,
  "close":166.3,
  "volume":1181806
}
"""
