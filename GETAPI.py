import requests
import json


class API:
    def __init__(self):
        self.api = "https://api.themeparks.wiki/v1"
        self.parks = {}
        self.shows = {}
        self.closed = {}
        self.attractions = {}

    def get_parks(self):
        try:
            parks_list_response = requests.get(self.api + "/destinations")
        except requests.exceptions.RequestException:
            return 0
        parks_list = json.loads(parks_list_response.text)
        for park_class in parks_list["destinations"]:
            for park in park_class["parks"]:
                self.parks[park["name"]] = park["id"]
        self.parks = dict(sorted(self.parks.items()))
        return self.parks

    def get_park(self, park_name):
        self.attractions = {}
        try:
            print(self.api + "/entity/" + self.parks[park_name] + '/live')
            park_response = requests.get(self.api + "/entity/" + self.parks[park_name] + '/live')
        except requests.exceptions.RequestException:
            return 0
        park = json.loads(park_response.text)
        for live in park["liveData"]:
            try:
                if live["queue"]["STANDBY"]["waitTime"] is not None:
                    self.attractions[live["name"]] = live["queue"]["STANDBY"]["waitTime"]
            except KeyError:
                pass

        # sort attractions by wait time from highest to lowest
        self.attractions = dict(sorted(self.attractions.items(), key=lambda item: item[1], reverse=True))

        return self.attractions

