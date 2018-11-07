import os

from flask import redirect

from app import create_app

config = os.getenv('APP_SETTINGS')
print(config)
app = create_app(config)


@app.route("/documentation")
def documentation():
    return redirect("https://storemanagerapiv22.docs.apiary.io/#")


if __name__ == "__main__":
    app.run()
