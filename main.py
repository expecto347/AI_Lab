import requests
import json
import GUI
import time

# Init Graphical User Interface
app = GUI.App()

# Get the list of parks
api = "https://api.themeparks.wiki/v1"
try:
    parks_list_response = requests.get(api + "/destinations")
except requests.exceptions.RequestException:
    print("Error: Unable to connect to the API")
    exit(1)

parks_list = json.loads(parks_list_response.text)
parks = {}
for park_class in parks_list["destinations"]:
    for park in park_class["parks"]:
        parks[park["name"]] = park["id"]

# sort parks by name
parks = dict(sorted(parks.items()))

# Update the list of parks in the GUI
app.update_parks(parks)
app.mainloop()