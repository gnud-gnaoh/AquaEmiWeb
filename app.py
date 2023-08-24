import json
import pycountry
import random
import requests
from flask import Flask, request, render_template, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow import fields, post_load
from models import db, WaterSource, WaterSourceSchema, WaterMeasurement, WaterMeasurementSchema, WaterMeasurementApp, WaterMeasurementAppSchema
from collections import defaultdict
from math import cos, asin, sqrt, pi

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
# app.config.from_pyfile('config.py')

db.init_app(app)

# for initializing the database
# with app.app_context():
#     db.create_all()

# water_source api
@app.route('/water_source', methods=['GET'])
def water_source_index():
    get_water_sources = WaterSource.query.all()
    water_source_schema = WaterSourceSchema(many=True)
    water_sources = water_source_schema.dump(get_water_sources)
    return make_response(jsonify({"water_source": water_sources}))

@app.route('/water_source/<id>', methods=['GET'])
def water_source_get_by_id(id):
    get_water_source = WaterSource.query.get(id)
    water_source_schema = WaterSourceSchema()
    water_source = water_source_schema.dump(get_water_source)
    return make_response(jsonify({"water_source": water_source}))

@app.route('/water_source', methods=['POST'])
def water_source_create():
    data = request.get_json()
    water_source_schema = WaterSourceSchema()
    water_source = water_source_schema.load(data)
    result = water_source_schema.dump(water_source.create())
    return make_response(jsonify({"water_source": result}), 200)

@app.route('/water_source/<id>', methods=['PUT'])
def water_source_update_by_id(id):
    data = request.get_json()
    get_water_source = WaterSource.query.get(id)
    if data.get('latitude'):
        get_water_source.latitude = data['latitude']
    if data.get('longitude'):
        get_water_source.longitude = data['longitude']
    if data.get('name'):
        get_water_source.name = data['name']
    if data.get('country'):
        get_water_source.country = data['country']    
    db.session.add(get_water_source)
    db.session.commit()
    water_source_schema = WaterSourceSchema(only=['id', 'latitude', 'longitude', 'name', 'country'])
    water_source = water_source_schema.dump(get_water_source)
    return make_response(jsonify({"water_source": water_source}))

@app.route('/water_source/<id>', methods=['DELETE'])
def water_source_delete_by_id(id):
    get_water_source = WaterSource.query.get(id)
    db.session.delete(get_water_source)
    db.session.commit()
    return make_response("", 204)
    
# water measurement api
@app.route('/measure', methods=['GET'])
def water_measurement_index():
    get_water_measurements = WaterMeasurement.query.all()
    water_measurement_schema = WaterMeasurementSchema(many=True)
    water_measurements = water_measurement_schema.dump(get_water_measurements)
    return make_response(jsonify({"water_measurements": water_measurements}))

@app.route('/measure/<id>', methods=['GET'])
def water_measurement_get_by_id(id):
    get_water_measurement = WaterMeasurement.query.get(id)
    water_measurement_schema = WaterMeasurementSchema()
    water_measurement = water_measurement_schema.dump(get_water_measurement)
    return make_response(jsonify({"water_measurement": water_measurement}))

@app.route('/measure', methods=['POST'])
def water_measurement_create():
    data = request.get_json()
    water_measurement_schema = WaterMeasurementSchema()
    water_measurement = water_measurement_schema.load(data)
    result = water_measurement_schema.dump(water_measurement.create())
    return make_response(jsonify({"water_measurement": result}), 200)

@app.route('/measure/<id>', methods=['PUT'])
def water_measurement_update_by_id(id):
    data = request.get_json()
    get_water_measurement = WaterMeasurement.query.get(id)
    if data.get('WaterSourceid'):
        get_water_measurement.WaterSourceid = data['WaterSourceid']
    if data.get('ph'):
        get_water_measurement.ph = data['ph']
    if data.get('turbidity'):
        get_water_measurement.turbidity = data['turbidity']
    if data.get('conductivity'):
        get_water_measurement.conductivity = data['conductivity']
    if data.get('temperature'):
        get_water_measurement.temperature = data['temperature']
    if data.get('flow'):
        get_water_measurement.temperature = data['flow']
    db.session.add(get_water_measurement)
    db.session.commit()
    water_measurement_schema = WaterMeasurementSchema(only=['id', 'WaterSourceid', 'ph', 'turbidity', 'conductivity', 'temperature', 'flow', 'datetime'])
    water_measurement = water_measurement_schema.dump(get_water_measurement)
    return make_response(jsonify({"water_measurement": water_measurement}))

@app.route('/measure/<id>', methods=['DELETE'])
def water_measurement_delete_by_id(id):
    get_water_measurement = WaterMeasurement.query.get(id)
    db.session.delete(get_water_measurement)
    db.session.commit()
    return make_response("", 204)

# water measurement app api
@app.route('/measureapp', methods=['GET'])
def water_measurement_app_index():
    get_water_measurements = WaterMeasurementApp.query.all()
    water_measurement_schema = WaterMeasurementAppSchema(many=True)
    water_measurements = water_measurement_schema.dump(get_water_measurements)
    return make_response(jsonify({"water_measurements_app": water_measurements}))

@app.route('/measureapp/<id>', methods=['GET'])
def water_measurement_app_get_by_id(id):
    get_water_measurement = WaterMeasurementApp.query.get(id)
    water_measurement_schema = WaterMeasurementAppSchema()
    water_measurement = water_measurement_schema.dump(get_water_measurement)
    return make_response(jsonify({"water_measurement_app": water_measurement}))

@app.route('/measureapp', methods=['POST'])
def water_measurement_app_create():
    data = request.get_json()
    water_measurement_schema = WaterMeasurementAppSchema()
    water_measurement = water_measurement_schema.load(data)
    result = water_measurement_schema.dump(water_measurement.create())
    return make_response(jsonify({"water_measurement_app": result}), 200)

@app.route('/measureapp/<id>', methods=['PUT'])
def water_measurement_app_update_by_id(id):
    data = request.get_json()
    get_water_measurement = WaterMeasurementApp.query.get(id)
    if data.get('latitude'):
        get_water_measurement.latitude = data['latitude']
    if data.get('longitude'):
        get_water_measurement.longitude = data['longitude']
    if data.get('turbidity'):
        get_water_measurement.turbidity = data['turbidity']
    if data.get('color'):
        get_water_measurement.color = data['color']
    db.session.add(get_water_measurement)
    db.session.commit()
    water_measurement_schema = WaterMeasurementAppSchema(only=['id', 'latitude', 'longitude', 'WaterSourceid', 'turbidity', 'color', 'datetime'])
    water_measurement = water_measurement_schema.dump(get_water_measurement)
    return make_response(jsonify({"water_measurement_app": water_measurement}))

@app.route('/measureapp/<id>', methods=['DELETE'])
def water_measurement_app_delete_by_id(id):
    get_water_measurement = WaterMeasurementApp.query.get(id)
    db.session.delete(get_water_measurement)
    db.session.commit()
    return make_response("", 204)

# Views

# standard_values = {'ph':8.5,
#             'turbidity':5, 
#             'conductivity':300,
#             'BOD':5, # is the data measure in ppm?
#             'DO':5,
#             'temperature':20}
standard_values =   [8.5,50,300,40,5]
ideal_values =      [7  ,0,0  ,0,14.6]

def calculate_WQI(data):
    standard_values_inverse = map(lambda x:1/x, standard_values)
    K = 1 / sum(standard_values_inverse)
    W = list(map(lambda x:K/x, standard_values))

    V = []
    # V.append(data['ph'])
    # V.append(data['turbidity'])
    # V.append(data['conductivity'])
    # V.append(data['BOD'])
    # V.append(data['DO'])
    V.append(data.ph)
    V.append(data.turbidity)
    V.append(data.conductivity)
    V.append(data.BOD)
    V.append(data.DO)
    
    vs = [0 for _ in range(5)]
    for i in range(5):
        if ideal_values[i] != 0:
            vs[i] = abs(V[i] - ideal_values[i]) / abs(standard_values[i] - ideal_values[i])
        else:
            vs[i] = V[i] / standard_values[i]

    Q = list(map(lambda x:100*x, vs))
    WQ = [W[i] * Q[i] for i in range(5)]
    WQI = sum(WQ) / sum(W)
    
    return WQI

# uses https://ipapi.co/api/
def get_ip():
    response = requests.get('https://api.ipify.org?format=json').json()
    print(response)
    return response["ip"]

def get_location():
    ip_address = get_ip()
    response = requests.get(f'https://geo.ipify.org/api/v2/country,city?apiKey=at_qPDqGnk8tasuDwZiO8RH5g5vwaN0W&ipAddress={ip_address}').json().get("location")
    print(response, response.get("city"))
    location_data = {
        "city": response.get("city"),
        "region": response.get("region"),
        "country_code": response.get("country"),
        "latitude": response.get("lat"),
        "longitude": response.get("lng")
    }
    print(location_data)
    return location_data

def distance(lat1, lon1, lat2, lon2):
    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)

    r = 6371 # km
    p = pi / 180

    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 2 * r * asin(sqrt(a))

def cleanup_name(name):
    parts = name.split(',')
    # remove suffix until enough characters
    char_count = sum(len(i) for i in parts)
    LIMIT = 30
    while char_count > LIMIT and len(parts) > 1:
        char_count -= len(parts[-1])
        del(parts[-1])
    return ','.join(parts)

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def home_page():
    watermeasurements = WaterMeasurement.query.all()
    
    data = []
    for measure in watermeasurements:
        watersource = WaterSource.query.get(measure.WaterSourceid)
        data.append([watersource.latitude, watersource.longitude, calculate_WQI(measure)])

    watersources = WaterSource.query.all()
    countries_data_map = defaultdict(list)
    watersources_data = []
    for watersource in watersources:
        if len(watersource.measurements) == 0:
            continue
        country = watersource.country # TODO: change to country code
        name = watersource.name # TODO: change to name
        followers = random.randrange(0, 1000)
        quality = int(calculate_WQI(watersource.measurements[-1]))
        countries_data_map[country].append(quality)
        watersources_data.append({'name': name, 'quality': int(quality), 'followers': followers})
    
    countries_data = []
    for country, quality_list in countries_data_map.items():
        quality = int(sum(quality_list) / len(quality_list))
        followers = random.randrange(0, 1000) # to be implemented
        countries_data.append({'id': 0, 'country': country, 'name': country, 'quality': quality, 'followers': followers})

    countries_data.sort(key=lambda d: d['quality'])
    countries_data = countries_data[:10] # take top 10

    # renumber id
    for id, val in enumerate(countries_data):
        val['id'] = id + 1

    # get location of request and find closest water source
    location_data = get_location()
    print(location_data)

    closest_watersource = watersources[0]
    for watersource in watersources:
        if distance(location_data['latitude'], location_data['longitude'], closest_watersource.latitude, closest_watersource.longitude) \
        > distance(location_data['latitude'], location_data['longitude'], watersource.latitude, watersource.longitude):
            closest_watersource = watersource
    
    # current = {'name': 'Sai Gon River', 'country': 'Vietnam', 'temperature': 20, 'quality': 201, 'flow': 12.23, 'turbidity': 5.23}
    current = {
        'name': closest_watersource.name,
        'display_name': cleanup_name(closest_watersource.name),
        'country': closest_watersource.country, 
        'temperature': int(closest_watersource.measurements[-1].temperature), 
        'quality': int(calculate_WQI(closest_watersource.measurements[-1])), 
        'flow': round(closest_watersource.measurements[-1].flow, 2),
        'turbidity': round(closest_watersource.measurements[-1].turbidity,2)
    }
    return render_template('index.html', data=json.dumps(data), countries_data=countries_data, current=current, watersources_data=watersources_data)

@app.route('/map', methods=['GET'])
def map_page():
    watermeasurements = WaterMeasurement.query.all()
    # with open('static/measurements.json') as data_file:
    #     file_content = data_file.read()

    # watermeasurements = json.loads(file_content)

    data = []
    for measure in watermeasurements:
        watersource = WaterSource.query.get(measure.WaterSourceid)
        quality = int(calculate_WQI(watersource.measurements[-1]))
        data.append([watersource.latitude, watersource.longitude, quality])

    watersources = WaterSource.query.all()
    watersources_data = []
    for watersource in watersources:
        if len(watersource.measurements) == 0:
            continue
        name = watersource.name # TODO: find nearest river?
        quality = int(calculate_WQI(watersource.measurements[-1]))
        followers = random.randrange(0, 1000) # to be implemented
        watersources_data.append({'name': name, 'quality': quality, 'followers': followers})
    return render_template('map.html', data=json.dumps(data), watersources_data=watersources_data)

@app.route('/map_earth', methods=['GET'])
def earth_page():
    watermeasurements = WaterMeasurement.query.all()
    
    features = []
    for measure in watermeasurements:
        watersource = WaterSource.query.get(measure.WaterSourceid)
        quality = int(calculate_WQI(watersource.measurements[-1]))
        features.append({
            "type": "Feature",
            "properties": {"mag": quality},
            "geometry": {
                "type": "Point",
                "coordinates": [watersource.longitude, watersource.latitude]
            }
        })

    data = {
        "type": "FeatureCollection",
        "features": features
    }

    watersources = WaterSource.query.all()
    watersources_data = []
    for watersource in watersources:
        if len(watersource.measurements) == 0:
            continue
        name = watersource.name # TODO: find nearest river?
        quality = int(calculate_WQI(watersource.measurements[-1]))
        followers = random.randrange(0, 1000) # to be implemented
        watersources_data.append({'name': name, 'quality': quality, 'followers': followers})
    return render_template('map_earth.html', data=json.dumps(data), watersources_data=watersources_data)

@app.route('/rankings', methods=['GET'])
def rank_page():  
    watersources = WaterSource.query.all()
    countries_data_map = defaultdict(list)
    watersources_data = []
    for watersource in watersources:
        if len(watersource.measurements) == 0:
            continue
        country = watersource.country # TODO: change to country code
        name = watersource.name # TODO: change to name
        quality = int(calculate_WQI(watersource.measurements[-1]))
        countries_data_map[country].append(quality)
        followers = random.randrange(0, 1000) # to be implemented
        watersources_data.append({'name': name, 'quality': int(quality), 'followers': followers})

    countries_data = []
    for country, quality_list in countries_data_map.items():
        quality = int(sum(quality_list) / len(quality_list))
        followers = random.randrange(0, 1000) # to be implemented
        countries_data.append({'id': 0, 'country': country, 'name': country, 'quality': quality, 'followers': followers})

    countries_data.sort(key=lambda d: d['quality'])
    countries_data = countries_data[:10] # take top 10

    # renumber id
    for id, val in enumerate(countries_data):
        val['id'] = id + 1

    return render_template('rankings.html', data=countries_data, watersources_data=watersources_data)

@app.route('/news', methods=['GET'])
def new_page():
    watersources = WaterSource.query.all()
    watersources_data = []
    for watersource in watersources:
        if len(watersource.measurements) == 0:
            continue
        name = watersource.name # TODO: find nearest river?
        quality = int(calculate_WQI(watersource.measurements[-1]))
        followers = random.randrange(0, 1000) # to be implemented
        watersources_data.append({'name': name, 'quality': quality, 'followers': followers})

    return render_template('news.html', watersources_data=watersources_data)

@app.route('/travel', methods=['GET'])
def travel_page():
    watersources = WaterSource.query.all()
    watersources_data = []
    for watersource in watersources:
        if len(watersource.measurements) == 0:
            continue
        name = watersource.name # TODO: find nearest river?
        quality = int(calculate_WQI(watersource.measurements[-1]))
        followers = random.randrange(0, 1000) # to be implemented
        watersources_data.append({'name': name, 'quality': quality, 'followers': followers})
    return render_template('travel.html', watersources_data=watersources_data)

@app.route('/details/<rivername>', methods=['GET'])
def detail_page(rivername):
    # find watersource by name
    watersources = WaterSource.query.all()
    data = {}
    watersources_data = []
    for watersource in watersources:
        if len(watersource.measurements) == 0:
            continue
        id = watersource.id
        country = watersource.country # TODO: change to country code
        name = watersource.name # TODO: find nearest river?
        quality = int(calculate_WQI(watersource.measurements[-1]))
        flow = round(watersource.measurements[-1].flow, 2)
        temperature = int(watersource.measurements[-1].temperature)
        turbidity = round(watersource.measurements[-1].turbidity, 2)
        followers = random.randrange(0, 1000) # to be implemented
        if watersource.name == rivername:
            data = {'id': id, 'country': country, 'name': name, 'quality': quality, 'followers': followers, 'temperature': temperature, 'flow': flow, 'turbidity': turbidity}
        watersources_data.append({'name': name, 'quality': quality, 'followers': followers})

    return render_template('details.html', rivername=rivername, data=data, watersources_data=watersources_data)

@app.route('/info', methods=['GET'])
def info_page():
    watersources = WaterSource.query.all()
    watersources_data = []
    for watersource in watersources:
        if len(watersource.measurements) == 0:
            continue
        name = watersource.name # TODO: find nearest river?
        quality = int(calculate_WQI(watersource.measurements[-1]))
        followers = random.randrange(0, 1000) # to be implemented
        watersources_data.append({'name': name, 'quality': quality, 'followers': followers})
    return render_template('info.html', watersources_data=watersources_data)

@app.route('/article1', methods=['GET'])
def article1_page():
    watersources = WaterSource.query.all()
    watersources_data = []
    for watersource in watersources:
        if len(watersource.measurements) == 0:
            continue
        name = watersource.name # TODO: find nearest river?
        quality = int(calculate_WQI(watersource.measurements[-1]))
        followers = random.randrange(0, 1000) # to be implemented
        watersources_data.append({'name': name, 'quality': quality, 'followers': followers})
    return render_template('article1.html', watersources_data=watersources_data)

@app.route('/article2', methods=['GET'])
def article2_page():
    watersources = WaterSource.query.all()
    watersources_data = []
    for watersource in watersources:
        if len(watersource.measurements) == 0:
            continue
        name = watersource.name # TODO: find nearest river?
        quality = int(calculate_WQI(watersource.measurements[-1]))
        followers = random.randrange(0, 1000) # to be implemented
        watersources_data.append({'name': name, 'quality': quality, 'followers': followers})
    return render_template('article2.html', watersources_data=watersources_data)

@app.route('/article3', methods=['GET'])
def article3_page():
    watersources = WaterSource.query.all()
    watersources_data = []
    for watersource in watersources:
        if len(watersource.measurements) == 0:
            continue
        name = watersource.name # TODO: find nearest river?
        quality = int(calculate_WQI(watersource.measurements[-1]))
        followers = random.randrange(0, 1000) # to be implemented
        watersources_data.append({'name': name, 'quality': quality, 'followers': followers})
    return render_template('article3.html', watersources_data=watersources_data)

@app.route('/article4', methods=['GET'])
def article4_page():
    watersources = WaterSource.query.all()
    watersources_data = []
    for watersource in watersources:
        if len(watersource.measurements) == 0:
            continue
        name = watersource.name # TODO: find nearest river?
        quality = int(calculate_WQI(watersource.measurements[-1]))
        followers = random.randrange(0, 1000) # to be implemented
        watersources_data.append({'name': name, 'quality': quality, 'followers': followers})
    return render_template('article4.html', watersources_data=watersources_data)

@app.route('/article5', methods=['GET'])
def article5_page():
    watersources = WaterSource.query.all()
    watersources_data = []
    for watersource in watersources:
        if len(watersource.measurements) == 0:
            continue
        name = watersource.name # TODO: find nearest river?
        quality = int(calculate_WQI(watersource.measurements[-1]))
        followers = random.randrange(0, 1000) # to be implemented
        watersources_data.append({'name': name, 'quality': quality, 'followers': followers})
    return render_template('article5.html', watersources_data=watersources_data)

if __name__ == '__main__':
    app.run()