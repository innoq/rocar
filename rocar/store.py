from textwrap import dedent

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

vehicles = { # by location -- XXX: why not simply an attribute?
    "BER": [
        {
            "id": 1,
            "make": "BMW",
            "model": "5-Series",
            "classes": ["luxury"],
            "passengers": 5,
            "cost": 257.12,
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
            "extras": []
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
            "extras": []
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
