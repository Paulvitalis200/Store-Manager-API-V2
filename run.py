import os

from app import create_app
from flask import redirect

config = os.getenv('APP_SETTINGS')
app = create_app('development')


@app.route("/documentation")
def documentation():
    return redirect("https://storemanagerapi.docs.apiary.io/#")


if __name__ == "__main__":
    app.run()
