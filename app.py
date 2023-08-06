import json
from flask import Flask, request, render_template, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow import fields, post_load
from models import db, WaterSource, WaterSourceSchema, WaterMeasurement, WaterMeasurementSchema, WaterMeasurementApp, WaterMeasurementAppSchema
import pycountry
import random

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

db.init_app(app)

# would this still work?
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
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def home_page():
    watermeasurements = WaterMeasurement.query.all()
    
    data = []
    for measure in watermeasurements:
        watersource = WaterSource.query.get(measure.WaterSourceid)
        data.append([watersource.longitude, watersource.latitude, abs(measure.ph - 7)])

    watersources = WaterSource.query.all()
    countries_data = []
    for watersource in watersources:
        if len(watersource.measurements) == 0:
            continue
        id = watersource.id
        country = watersource.country
        name = pycountry.countries.get(alpha_2=country).name
        quality = int(sum(abs(measurement.ph - 7) * 50 for measurement in watersource.measurements) / len(watersource.measurements))
        followers = random.randrange(0, 1000) # to be implemented
        countries_data.append({'id': id, 'country': country, 'name': name, 'quality': quality, 'followers': followers})

    countries_data.sort(key=lambda d: d['quality'])
    countries_data = countries_data[:10] # take top 10

    # renumber id
    for id, val in enumerate(countries_data):
        val['id'] = id + 1

    # get location of request and find closest water source
    
    current = {'name': 'Sai Gon River', 'country': 'Vietnam', 'temperature': 20, 'quality': 201, 'flow': 12.23, 'turbidity': 5.23}
    return render_template('index.html', data=json.dumps(data), countries_data=countries_data, current=current)

@app.route('/map', methods=['GET'])
def map_page():
    watermeasurements = WaterMeasurement.query.all()
    
    data = []
    for measure in watermeasurements:
        watersource = WaterSource.query.get(measure.WaterSourceid)
        data.append([watersource.longitude, watersource.latitude, abs(measure.ph - 7)])

    return render_template('map.html', data=json.dumps(data))

@app.route('/map_earth', methods=['GET'])
def earth_page():
    watermeasurements = WaterMeasurement.query.all()
    
    features = []
    for measure in watermeasurements:
        watersource = WaterSource.query.get(measure.WaterSourceid)
        features.append({
            "type": "Feature",
            "properties": {"mag": abs(measure.ph - 7) * 100}, # currently set the quality function just from the ph
            "geometry": {
                "type": "Point",
                "coordinates": [watersource.longitude, watersource.latitude]
            }
        })

    data = {
        "type": "FeatureCollection",
        "features": features
    }

    return render_template('map_earth.html', data=json.dumps(data))

@app.route('/rankings', methods=['GET'])
def rank_page():
    watersources = WaterSource.query.all()
    data = []
    for watersource in watersources:
        if len(watersource.measurements) == 0:
            continue
        id = watersource.id
        country = watersource.country
        name = pycountry.countries.get(alpha_2=country).name
        quality = int(sum(abs(measurement.ph - 7) * 50 for measurement in watersource.measurements) / len(watersource.measurements)) # currently set the quality function just from the ph
        followers = random.randrange(0, 1000) # to be implemented
        data.append({'id': id, 'country': country, 'name': name, 'quality': quality, 'followers': followers})

    data.sort(key=lambda d: d['quality'])

    # renumber id
    for id, val in enumerate(data):
        val['id'] = id + 1
    
    return render_template('rankings.html', data=data)

@app.route('/news', methods=['GET'])
def new_page():
    return render_template('news.html')

@app.route('/travel', methods=['GET'])
def travel_page():
    return render_template('travel.html')

@app.route('/details/<rivername>', methods=['GET'])
def detail_page(rivername):
    # find watersource by name
    watersources = WaterSource.query.all()
    data = {}
    for watersource in watersources:
        if len(watersource.measurements) == 0:
            continue
        id = watersource.id
        country = watersource.country
        name = pycountry.countries.get(alpha_2=country).name

        # currently taking average or first measure just for testing, should be taking the latest measurement
        quality = int(sum(abs(measurement.ph - 7) * 50 for measurement in watersource.measurements) / len(watersource.measurements))
        flow = round(watersource.measurements[0].flow, 2)
        temperature = int(watersource.measurements[0].temperature)
        turbidity = round(watersource.measurements[0].turbidity, 2)
        followers = random.randrange(0, 1000) # to be implemented
        if watersource.name == rivername:
            data = {'id': id, 'country': country, 'name': name, 'quality': quality, 'followers': followers, 'temperature': temperature, 'flow': flow, 'turbidity': turbidity}

    return render_template('details.html', rivername=rivername, data=data)

@app.route('/info', methods=['GET'])
def info_page():
    return render_template('info.html')

if __name__ == '__main__':
    app.run()