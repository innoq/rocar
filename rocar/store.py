from textwrap import dedent

from flask import url_for

from . import i18n


def search(query):
    query = query.lower()
    results = []

    for location_id, meta in locations.items():
        if (query in meta["summary"].lower() or
                query in meta["details"].lower()):
            results.append({
                "type": "location",
                "name": i18n.gettext(location_id), # XXX: i18n does not belong here
                "desc": meta["summary"],
                "url": url_for("location", location_id=location_id)
            })

    for make, models in vehicle_info.items():
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

    return results


def get_vehicles(location_ids=None):
    location_ids = location_ids or vehicles.keys()

    vehicle_classes = set()
    vehicle_extras = set()
    _vehicles = []
    for location_id in location_ids:
        for vehicle in vehicles.get(location_id, []):
            vehicle_classes.update(vehicle.get("classes", []))
            vehicle_extras.update(vehicle.get("extras", []))
            _vehicles.append(vehicle)

    return _vehicles, vehicle_classes, vehicle_extras


def filter_vehicles(vehicles, vehicle_classes, vehicle_extras):
    for vehicle in vehicles:
        classes = set(vehicle.get("classes", []))
        extras = set(vehicle.get("extras", []))
        if ((not vehicle_classes or classes.intersection(vehicle_classes)) and
                (not vehicle_extras or extras.issuperset(vehicle_extras))):
            yield vehicle


locations = {
    "BER": {
        "coordinates": (52.516667, 13.383333),
        "desc": dedent("""
            located right next to the airport in Germany's capital - beware of
            construction vehicles
            ----
            Opening Hours:
            Mo - Fr   07:00 - 21:00
            Sa        08:00 - 16:00
            """).strip()
    },
    "LAX": {
        "coordinates": (34.05, -118.25),
        "desc": dedent("""
            just a short drive from the Hollywood Hills, we recommend you bring
            a camera for lasting impressions
            ----
            open all day, every day
            """).strip(),
    },
    "LCY": {
        "coordinates": (51.507222, -0.1275),
        "desc": dedent("""
            conveniently located in zone 3 - note that roads might be subject
            to congestion charge
            ----
            Opening Hours:
            Mo - Fr   09:00 - 17:00
            Sa        09:00 - 12:00
            """).strip()
    }
}
for location_id, data in locations.items():
    summary, details = data["desc"].split("\n----\n")
    location = locations[location_id]
    location["summary"] = summary
    location["details"] = details
    location.pop("desc")

vehicle_info = {
    "BMW": {
        "7-Series": "chauffeur not included"
    },
    "Audi": {
        "S6": "for when you can't afford a Beamer"
    },
    "VW": {
        "Golf": "compensatory customizations optional"
    },
    "Toyota": {
        "Corolla": "zzzZZZzzz"
    },
    "Ford": {
        "Mustang": "from 60 to 0 gallons in 3.4 minutes"
    },
    "Lotus": {
        "Elise": "almost like driving a go-kart"
    },
    "Jaguar": {
        "XF": "requires proof of age (60 upwards)"
    }
}

vehicles = { # by location -- XXX: why not simply an attribute?
    "BER": [
        {
            "id": 1,
            "make": "BMW",
            "model": "7-Series",
            "classes": ["luxury"],
            "passengers": 5,
            "cost": 357.12,
            "extras": ["ac", "gps", "hud"]
        }, {
            "id": 2,
            "make": "Audi",
            "model": "S6",
            "classes": ["sports", "luxury"],
            "passengers": 5,
            "cost": 234.28,
            "extras": ["4wd", "ac", "gps"]
        }, {
            "id": 3,
            "make": "VW",
            "model": "Golf",
            "classes": ["compact"],
            "passengers": 4,
            "cost": 160.88,
            "extras": ["ac", "gps"]
        }, {
            "id": 4,
            "make": "Toyota",
            "model": "Corolla",
            "classes": ["sedan"],
            "passengers": 4,
            "cost": 153.70,
            "extras": ["ac", "gps"]
        }
    ],
    "LAX": [
        {
            "id": 5,
            "make": "Ford",
            "model": "Mustang",
            "classes": ["sports"],
            "passengers": 2,
            "cost": 190.33,
            "extras": ["ac"]
        }
    ],
    "LCY": [
        {
            "id": 6,
            "make": "Lotus",
            "model": "Elise",
            "classes": ["sports"],
            "passengers": 2,
            "cost": 279.49,
            "extras": ["ac"]
        }, {
            "id": 7,
            "make": "Jaguar",
            "model": "XF",
            "classes": ["luxury"],
            "passengers": 5,
            "cost": 290.65,
            "extras": ["ac", "gps"]
        }
    ]
}
