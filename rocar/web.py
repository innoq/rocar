from flask import Flask, render_template, redirect, url_for, request

from . import store


app = Flask(__name__)


@app.route("/")
def frontpage():
    return redirect(url_for("catalog"))


@app.route("/catalog")
def catalog(): # TODO: move filtering into store module
    selected_locations = set(request.args.getlist("location")) # XXX: order matters (start vs. end)
    locations = [Location(id, name, store.coordinates[id],
            id in selected_locations) for id, name in store.locations.items()]

    selected_vehicle_classes = set(request.args.getlist("vehicle-class"))
    vehicle_classes = set()
    selected_vehicle_extras = set(request.args.getlist("vehicle-extra"))
    vehicle_extras = set()
    vehicles = []
    for location_id in (selected_locations or store.locations.keys()):
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
                    vehicle["cost"], str(vehicle["id"]) == selected_vehicle_id)
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

    selection = {
        "location": selected_locations,
        "vehicle-class": selected_vehicle_classes,
        "vehicle-extra": selected_vehicle_extras,
        "vehicle": [selected_vehicle_id]
    }
    return render("catalog.html", selection_state=selection, locations=locations,
            vehicle_classes=vehicle_classes, vehicle_extras=vehicle_extras,
            vehicles=vehicles, vehicle=selected_vehicle)


def render(template, *args, **kwargs):
    kwargs["styles"] = (url_for("static", filename="styles/%s" % name)
            for name in ["layout.css", "main.css"])
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

    def __init__(self, id, name, coordinates, selected=False):
        super().__init__(id, name, selected)
        self.coordinates = coordinates

    def __repr__(self):
        return "%s %s>" % (super().__repr__()[:-1], self.coordinates)


class Vehicle(Selectable):

    def __init__(self, id, name, cost, selected=False):
        super().__init__(id, name, selected)
        self.cost = cost

    def __repr__(self):
        return "%s %s>" % (super().__repr__()[:-1], self.cost)
