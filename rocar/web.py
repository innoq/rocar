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

    selected_locations = set(request.args.getlist("location")) # XXX: order matters (start vs. end)
    locations = [Location(id, store.locations[id]["coordinates"],
            id in selected_locations) for id in location_ids]

    selected_vehicle_classes = set(request.args.getlist("vehicle-class"))
    vehicle_classes = set()
    selected_vehicle_extras = set(request.args.getlist("vehicle-extra"))
    vehicle_extras = set()
    vehicles = []
    for location_id in (selected_locations or location_ids):
        for vehicle in store.vehicles.get(location_id, []):
            classes = [Selectable(id, id, id in selected_vehicle_classes)
                    for id in vehicle.get("classes", [])]
            vehicle_classes.update(classes)

            extras = [Selectable(id, id, id in selected_vehicle_extras)
                    for id in vehicle.get("extras", [])]
            vehicle_extras.update(extras)

            vehicles.append(vehicle) # XXX: should only take into account start location?

    selected_vehicle_id = request.args.get("vehicle", None)
    vehicles = [Vehicle(vehicle["id"],
                    "%s %s" % (vehicle["make"], vehicle["model"]),
                    vehicle["passengers"], vehicle["cost"],
                    str(vehicle["id"]) == selected_vehicle_id)
            for vehicle in vehicles if # XXX: inefficient
            (
                len(selected_vehicle_classes) == 0
                or
                set(vehicle.get("classes", [])).
                        intersection(selected_vehicle_classes)
            ) and (
                len(selected_vehicle_extras) == 0 or
                set(vehicle.get("extras", [])).
                        issuperset(selected_vehicle_extras)
            )
    ]
    selected_vehicle = next((v for v in vehicles if v.selected), None) # XXX: inefficient

    current_url = None
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        current_url = url_for("catalog", **request.args) # XXX: hacky?

    selection = {
        "location": selected_locations,
        "vehicle-class": selected_vehicle_classes,
        "vehicle-extra": selected_vehicle_extras,
        "vehicle": [selected_vehicle_id] if selected_vehicle_id else []
    }
    return render("catalog.html", current_url=current_url,
            selection_state=selection, locations=locations,
            vehicle_classes=vehicle_classes, vehicle_extras=vehicle_extras,
            vehicles=vehicles, vehicle=selected_vehicle)


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


def render(template, *args, **kwargs):
    kwargs["styles"] = [url_for("static", filename=name) for name
            in ["styles/layout.css", "styles/main.css", "vendor/leaflet.css"]]
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
