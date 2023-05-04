import requests
import json


class API:
    def __init__(self):
        self.api = "https://api.themeparks.wiki/v1"
        self.parks = {}
        self.closed = []
        self.attractions = {}

    def get_parks(self):
        """
        Returns a dictionary of parks
        :return:
        """
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
        """
        Returns a dictionary of attractions and their wait times
        :param park_name:
        :return: attractions, closed
        """
        self.attractions = {}
        self.closed = []
        try:
            # print(self.api + "/entity/" + self.parks[park_name] + '/live')
            park_response = requests.get(self.api + "/entity/" + self.parks[park_name] + '/live')
        except requests.exceptions.RequestException:
            return 0, 0
        park = json.loads(park_response.text)
        for live in park["liveData"]:
            if live["status"] == "CLOSED":
                self.closed.append(live["name"])
            elif live["entityType"] == "ATTRACTION":
                try:
                    if live["queue"]["STANDBY"]["waitTime"] is not None and live["status"] == "OPERATING":
                        self.attractions[live["name"]] = live["queue"]["STANDBY"]["waitTime"]
                except KeyError:
                    pass

        # sort attractions by wait time from highest to lowest
        self.attractions = dict(sorted(self.attractions.items(), key=lambda item: item[1], reverse=True))

        return self.attractions, self.closed

    def get_schedule(self, park_name):
        """
        Returns the closing and opening time of the park
        """
        try:
            print(self.api + '/entity/' + self.parks[park_name] + '/schedule')
            schedule_response = requests.get(self.api + '/entity/' + self.parks[park_name] + '/schedule')
        except requests.exceptions.RequestException:
            return 0, 0
        schedule = json.loads(schedule_response.text)
        return schedule["schedule"][1]["closingTime"], schedule["schedule"][1]["openingTime"]
