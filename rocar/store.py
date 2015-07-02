locations = {
    "BER": "Berlin",
    "LAX": "Los Angeles",
    "LCY": "London"
}

coordinates = { # latitude, longitude
    "BER": (52.516667, 13.383333),
    "LAX": (34.05, -118.25),
    "LCY": (51.507222, -0.1275)
}

vehicles = { # by location -- XXX: why not simply an attribute?
    "BER": [
        {
            "id": 1,
            "make": "BMW",
            "model": "5-Series",
            "classes": ["luxury"],
            "passengers": 5,
            "cost": 257.12,
            "extras": ["ac", "nav", "hud"]
        }, {
            "id": 2,
            "make": "Audi",
            "model": "S6",
            "classes": ["sports", "luxury"],
            "passengers": 5,
            "cost": 234.28,
            "extras": ["4wd", "ac", "nav"]
        }, {
            "id": 3,
            "make": "VW",
            "model": "Golf",
            "classes": ["compact"],
            "passengers": 4,
            "cost": 160.88,
            "extras": ["ac", "nav"]
        }, {
            "id": 4,
            "make": "Toyota",
            "model": "Corolla",
            "classes": ["sedan"],
            "passengers": 4,
            "cost": 153.70,
            "extras": ["ac", "nav"]
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
            "extras": ["ac", "nav"]
        }
    ]
}
