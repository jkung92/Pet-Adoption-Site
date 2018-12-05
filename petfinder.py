from secrets import API_Secret, API_Key
import requests


def get_random_pet():
    try:
        resp = requests.get(
            "http://api.petfinder.com/pet.getRandom",
            params={
                "format": "json",
                "key": API_Key,
                "output": "basic"
            })

        name = resp.json()["petfinder"]["pet"]["name"]["$t"]
        age = resp.json()["petfinder"]["pet"]["age"]["$t"]
        photo_url = resp.json(
        )["petfinder"]["pet"]["media"]["photos"]["photo"][3]["$t"]

        return {"name": name, "age": age, "photo_url": photo_url}
    except (ValueError, IndexError):
        return {"error": "Request failed"}