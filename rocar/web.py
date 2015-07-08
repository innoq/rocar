from flask import Flask, render_template, redirect, abort, url_for, request

from . import store
from . import i18n


app = Flask(__name__)
# l10n
app.jinja_env.add_extension("jinja2.ext.i18n")
app.jinja_env.install_gettext_callables(i18n.gettext, i18n.ngettext)


@app.route("/")
def frontpage():
    return redirect(url_for("catalog"))


@app.route("/catalog")
def catalog(): # TODO: move filtering into store module
    location_ids = store.vehicles.keys()

    selected_location_ids = request.args.getlist("location") # NB: order matters
    selected_locations = [Location(id, store.locations[id]["coordinates"], True)
            for id in selected_location_ids]
    available_locations = [] if len(selected_locations) == 2 else [Location(id,
            store.locations[id]["coordinates"]) for id in location_ids]

    selected_vehicle_classes = set(request.args.getlist("vehicle-class"))
    selected_vehicle_extras = set(request.args.getlist("vehicle-extra"))
    vehicles, vehicle_classes, vehicle_extras = store.get_vehicles(
            selected_location_ids[0:1])

    selected_vehicle_id = request.args.get("vehicle", None)
    vehicles = [Vehicle(vehicle["id"],
                "%s %s" % (vehicle["make"], vehicle["model"]),
                vehicle["passengers"], vehicle["cost"],
                str(vehicle["id"]) == selected_vehicle_id)
            for vehicle in store.filter_vehicles(vehicles,
                    selected_vehicle_classes, selected_vehicle_extras)]
    selected_vehicle = next((v for v in vehicles if v.selected), None) # XXX: inefficient

    current_url = url_for("catalog", **request.args) if request.is_xhr else None # XXX: parameter handling hacky?
    selection = {
        "location": selected_location_ids,
        "vehicle-class": selected_vehicle_classes,
        "vehicle-extra": selected_vehicle_extras,
        "vehicle": [selected_vehicle_id] if selected_vehicle_id else []
    }
    return render("catalog.html", current_url=current_url,
            selection_state=selection, selected_locations=selected_locations,
            available_locations=available_locations,
            vehicle_classes=(Selectable(id, id, id in selected_vehicle_classes)
                    for id in vehicle_classes),
            vehicle_extras=(Selectable(id, id, id in selected_vehicle_extras)
                    for id in vehicle_extras),
            vehicles=vehicles, vehicle=selected_vehicle)


@app.route("/search")
def search(): # XXX: very inefficient
    query = request.args.get("q", None)
    message = None

    results = []
    if query:
        query = query.lower()

        for location_id, meta in store.locations.items():
            if (query in meta["summary"].lower() or
                    query in meta["details"].lower()):
                results.append({
                    "type": "location",
                    "name": i18n.gettext(location_id),
                    "desc": meta["summary"],
                    "url": url_for("location", location_id=location_id)
                })

        for make, models in store.vehicle_info.items():
            for model, desc in models.items():
                if (query in make.lower() or
                        query in model.lower() or
                        query in desc.lower()):
                    results.append({
                        "type": "vehicle",
                        "name": "%s %s" % (make, model),
                        "desc": desc,
                        "url": url_for("vehicle", make=make, model=model)
                    })

        if not results:
            message = "no results for '%s'" % query
    else:
        message = "current promotions"
        results = [{
            "type": "vehicle",
            "name": "VW Beetle",
            "desc": "feature creep",
            "url": url_for("frontpage") # TODO
        }, {
            "type": "vehicle",
            "name": "Ford F-150",
            "desc": "because sometimes there are pebbles on the road",
            "url": url_for("frontpage") # TODO
        }, {
            "type": "location",
            "name": "Sydney",
            "desc": "celebrating Shark Week, every week",
            "url": url_for("frontpage") # TODO
        }]

    return render("search.html", results=results, message=message)


@app.route("/locations/<location_id>")
def location(location_id):
    try:
        meta = store.locations[location_id]
    except KeyError:
        abort(404)

    location = {
        "id": location_id,
        "summary": meta["summary"],
        "details": meta["details"]
    }
    return render("location.html", location=location)


@app.route("/vehicles/<make>/<model>")
def vehicle(make, model):
    try:
        desc = store.vehicle_info[make][model]
    except KeyError:
        abort(404)

    return render("vehicle.html", make=make, model=model, desc=desc)


def render(template, *args, **kwargs):
    kwargs["xhr"] = request.is_xhr
    kwargs["styles"] = [url_for("static", filename="bundle.css")]
    kwargs["scripts"] = [url_for("static", filename="bundle.js")]
    return render_template(template, *args, **kwargs)


class Selectable:

    def __init__(self, id, name, selected=False):
        self.id = id
        self.name = name
        self.selected = selected

    def __lt__(self, other):
        return self.id < other.id

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return """<%s %s "%s" %s>""" % (self.__class__.__name__, self.id,
                self.name, "✓" if self.selected else "✗")


class Location(Selectable):

    def __init__(self, id, coordinates, selected=False):
        super().__init__(id, i18n.gettext(id), selected)
        self.coordinates = coordinates

    def __repr__(self):
        return "%s %s>" % (super().__repr__()[:-1], self.coordinates)


class Vehicle(Selectable):

    def __init__(self, id, name, passengers, cost, selected=False):
        super().__init__(id, name, selected)
        self.passengers = passengers
        self.cost = cost

    def __repr__(self):
        return "%s %s>" % (super().__repr__()[:-1], self.cost)
