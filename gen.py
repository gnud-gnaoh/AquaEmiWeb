import requests
import random
from faker import Faker
import json

# url = 'http://127.0.0.1:5000/water_source'
url = 'http://127.0.0.1:5000/measure'
fake = Faker()
Faker.seed(random.random())

tmp = [[1, 2, 3], [2, 3, 4], [4, 5, 6]]
print(json.dumps(tmp))

for _ in range(50):
    latitude = random.randrange(-90, 90)
    longitude = random.randrange(-180, 180)
    # name = fake.address()
    # country = fake.country_code()
    intensity = random.randrange(0, 1)

    # data = {'latitude':latitude, 'longitude':longitude, 'name':name, 'country':country}
    # WaterSourceid = random.randrange(1, 80)
    # ph = random.uniform(0, 14)
    # turbidity = random.random()
    # conductivity = random.random()
    # temperature = random.uniform(0, 100)
    # flow = random.random()

    # data = {'WaterSourceid':WaterSourceid, 'ph':ph, 'turbidity':turbidity, 'conductivity':conductivity, 'temperature':temperature, 'flow':flow}
    data = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {"mag": intensity},
            "geometry": {
                "type": "Point",
                "coordinates": [latitude, longitude, 100]
            }
        }]
    }
    response = requests.post(url, json=data)

    print(response.text)