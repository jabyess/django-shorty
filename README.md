# Django-Shorty

## A url shortener

Built using django!

### Endpoints

| URL                | method | description                                                                                                                                                          | returns                                                                               |
| ------------------ | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `/create`          | POST   | Creates a new shortened url if one doesn't exist already. The request body must be a json string with this format: `{"url": "http[s]://example.com/whatever/thing"}` | `{"shorturl" : "http[s]://domain.com/QprDmf0M"}`                                      |
| `/<shortid>`       | GET    | Looks up the url provided and redirects                                                                                                                              | A `302` redirect to the long url, or `404` if not found.                              |
| `/<shortid>/stats` | GET    | Retrieves stats for the provided short url                                                                                                                           | `{ "total_visits": 4, "created": "2019-11-08T18:43:22.007Z", "visits_per_day": 4.0 }` |

### Prerequisites

- Python 3.6 or higher
- pipenv
- postgreSQL 10 or higher

### Installation & Setup

- Clone this repo.
- `cd` to the cloned directory
- Install dependencies `pipenv install`
- Log in to the `psql` cli and create a database with user and permissions
  (change these as desired in settings.py)
  - `CREATE DATABASE urlshort;`
  - `CREATE USER urlshort WITH PASSWORD 'urlshort';`
  - `GRANT ALL PRIVILEGES ON DATABASE urlshort TO urlshort;`
- Launch the virtualenv with `pipenv shell`
- Run the django web server with `python3 manage.py runserver`
- Use your favorite API client to make requests!

### Notes on architecture

I originally started this using flask, because I thought "hey this is simple, I
don't need a whole ORM, I can just wing it". I got quickly overwhelmed by all
the research and choices and figuring out how to wire up a database to the flask
app. Plus I know django much better, so I was able to be much more productive.

My first django iteration had two models - Link and Stats. 