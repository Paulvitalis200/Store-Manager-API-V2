import os

from flask import redirect

from app import create_app

config = os.getenv('APP_SETTINGS')
app = create_app('development')


@app.route("/documentation")
def documentation():
    return redirect("https://storemanagerapi.docs.apiary.io/#")


if __name__ == "__main__":
    app.run()
