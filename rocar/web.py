from flask import Flask, render_template, redirect, url_for

from . import store


app = Flask(__name__)


@app.route("/")
def frontpage():
    return redirect(url_for("catalog"))


@app.route("/catalog")
def catalog():
    return render("catalog.html", locations=store.locations)


def render(template, *args, **kwargs):
    kwargs["styles"] = (url_for("static", filename="styles/%s" % name)
            for name in ["layout.css", "main.css"])
    return render_template(template, *args, **kwargs)
