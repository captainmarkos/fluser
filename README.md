### Flask User Service

Run as a Docker container:
```bash
$ docker build -t fluser .
$ docker run --detach -p 5000:5000 --name fluser fluser

# or
$ source bash_aliases.sh
$ rnr_fluser
```

If were run with `flask run`:
```bash
$ . venv/bin/activate
$ flask --app api init-db
$ flask --app api --debug run
```

Check the app is running
```bash
$ curl http://127.0.0.1:5000/status
```

#### The Database

To initialize the DB, run `init-db`
```bash
$ flask --app api init-db
```

Verify the DB has been initialized
```bash
$ sqlite3 instance/fluser.sqlite
sqlite> .tables
users

sqlite> .schema users
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

sqlite> .header on
sqlite> .mode table

sqlite> pragma table_info('users');
+-----+------------+-----------+---------+-------------------+----+
| cid |    name    |   type    | notnull |    dflt_value     | pk |
+-----+------------+-----------+---------+-------------------+----+
| 0   | id         | INTEGER   | 0       |                   | 1  |
| 1   | email      | TEXT      | 1       |                   | 0  |
| 2   | password   | TEXT      | 1       |                   | 0  |
| 3   | created_at | TIMESTAMP | 1       | CURRENT_TIMESTAMP | 0  |
+-----+------------+-----------+---------+-------------------+----+
```


#### About Responses

The return value from a view function is automatically converted into a response object for you. If the return value is a string it’s converted into a response object with the string as response body, a 200 OK status code and a text/html mimetype. If the return value is a dict or list, jsonify() is called to produce a response.  More...

[https://flask.palletsprojects.com/en/2.2.x/quickstart/#about-responses](https://flask.palletsprojects.com/en/2.2.x/quickstart/#about-responses}


#### Register New User

```bash
$ curl -v 'http://127.0.0.1:5000/auth/register' \
       -H 'Content-Type: application/json' \
       --data-raw '{"email": "bobby@foo.com", "password": "bar" }'

*   Trying 127.0.0.1:5000...
* Connected to 127.0.0.1 (127.0.0.1) port 5000 (#0)
> POST /auth/register HTTP/1.1
> Host: 127.0.0.1:5000
> User-Agent: curl/7.79.1
> Accept: */*
> Content-Type: application/json
> Content-Length: 49
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: Werkzeug/2.2.2 Python/3.10.6
< Date: Wed, 19 Oct 2022 05:36:39 GMT
< Content-Type: application/json
< Content-Length: 65
< Connection: close
<
{
  "success": "Email 'bobby@foo.com' successfully registered."
}
```


#### Fluser Docker Image

```bash
$ . venv/bin/activate
(venv) $ pip freeze > requirements.txt

$ cat requirements.txt
click==8.1.3
Flask==2.2.2
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.1
Werkzeug==2.2.2
```


#### DB Queries in Python CLI

[DB-API 2.0 interface for SQLite Databases](https://docs.python.org/3/library/sqlite3.html)
```python
>>> import sqlite3
>>> db = sqlite3.connect('instance/fluser.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
>>> db.row_factory = sqlite3.Row
>>> res = db.execute('SELECT * FROM users').fetchone()

>>> tuple(res)
(1, 'thor@yahoo.com', 'password', datetime.datetime(2022, 10, 19, 5, 48, 58))

>>> res['email']
'thor@yahoo.com'
>>> res['created_at']
datetime.datetime(2022, 10, 19, 5, 48, 58)
```

Setup the `Connection` object to use a custom `row_factory`. See [here](https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factory).
```python
>>> import sqlite3
>>> db = sqlite3.connect('instance/fluser.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)

>>> def dict_factory(cursor, row):
...     col_names = [col[0] for col in cursor.description]
...     return {key: value for key, value in zip(col_names, row)}
...
>>> db.row_factory = dict_factory
>>> res = db.execute('SELECT * FROM users').fetchone()
>>> print(res)
{'id': 1, 'email': 'thor@yahoo.com', 'password': 'password', 'created_at': datetime.datetime(2022, 10, 19, 5, 48, 58)}
>>> res['email']
'thor@yahoo.com'
```