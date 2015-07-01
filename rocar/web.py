from flask import Flask, render_template, redirect, url_for, request

from . import store


app = Flask(__name__)


@app.route("/")
def frontpage():
    return redirect(url_for("catalog"))


@app.route("/catalog")
def catalog():
    selected_locations = set(request.args.getlist("location")) # XXX: order matters (start vs. end)
    locations = [Location(id, name, store.coordinates[id],
            id in selected_locations) for id, name in store.locations.items()]

    return render("catalog.html", locations=locations)


def render(template, *args, **kwargs):
    kwargs["styles"] = (url_for("static", filename="styles/%s" % name)
            for name in ["layout.css", "main.css"])
    return render_template(template, *args, **kwargs)


class Location:

    def __init__(self, id, name, coordinates, selected=False):
        self.id = id
        self.name = name
        self.coordinates = coordinates
        self.selected = selected
