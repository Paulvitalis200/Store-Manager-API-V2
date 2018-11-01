import os

from app import create_app
from flask import redirect

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)


@app.route("/documentation")
def documentation():
    return redirect("https://storemanagerapi.docs.apiary.io/#")


if __name__ == "__main__":
    app.run()
