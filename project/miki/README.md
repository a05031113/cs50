# Miki

For the final project of [CS50](/learn/cs50.html), I wrote a Flask based
[ikiwiki](https://ikiwiki.info/) clone called Miki.

Miki is different from popular Wiki engines in that it do not save content in a
database. Instead it will generate HTML from markdown each time someone edits
the page and will save both markdown and HTML in there specified directories.
[Nginx](https://www.nginx.org/) will then simply serve static pages. This means
that readers of the wiki will only see the static pages which can be served
quickly and efficiently. However, for all the dynamic parts of the wiki, the
requests are forwarded to Miki and it will function accordingly.

Miki listens on some special routes and it will use the parameters passed to
handle the requests. Miki also include user based authentication and for that
it uses [SQLite](https://www.sqlite3.org/) database.

## Routes

* `/edit` &mdash; Editing pages
* `/auth/login` &mdash; Logging users in
* `/auth/logout` &mdash; Logout users
* `/auth/register` &mdash; Register new users
* `/auth/reset` &mdash; Reset password
