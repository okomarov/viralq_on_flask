# Build your viral queue page with flask
An example how to build a viral queue page with flask

For details and how to use, please read: [Build your own viral queue in Flask](https://medium.com/@olegkomarov_77860/build-your-own-viral-queue-in-flask-e64e90bbf3ca)

## Deploy on Heroku (free)
First, edit the `app.json` and replace the value of the `repository`:
```
"repository": "https://github.com/okomarov/viralq_on_flask"
```
with the URL to the forked repository.

Then, you will need to configure your email service and edit in `app.json` the values for the environment variables `MAIL_SERVER`, `MAIL_USERNAME`, `MAIL_PASSWORD` and `MAIL_PORT` accordingly.

Finally, click on the button:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
