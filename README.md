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

My first django iteration had two models - Link and Stats, with Stats having a
property called `visits`. I realized later (after reading more thoroughly) that
I needed to record each page visit historically, so I renamed `Stats` to `Visit`
and gave `visit` a datetime property with default timestamp. Now each visit is
its own row, which makes writing records much easier (they're stateless and I
don't have to do the incrementing/counting logic myself). This also makes
querying more flexible, since I am using sql commands (via the ORM) instead of
python business logic.

I spent a fair amount of time on validation - making sure the POST request
contained the right keys and that the url provided was a valid URL. I know there
are better ways to do this (you can pass the validator into the model) but it'll
require some more thought and research.

Also, its possible to cause a 500 error by sending malformed json, since I'm not
handling any exceptions around the parsing.

Given some more time, I'd like to add tests and figure out a more sane and
django-y way to handle all the validation.

Overall, this was a fun project and a good refresher for me on django.
