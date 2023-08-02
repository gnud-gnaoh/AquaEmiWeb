import datetime
from flask import Flask, request, render_template, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow import fields, post_load

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:bubudeptrai2006@localhost:3306/bucketlist'
app.secret_key = 'mmb'

db = SQLAlchemy(app)

### Models

# WaterSource
class WaterSource(db.Model):
    __tablename__ = 'WaterSources'
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    name = db.Column(db.String(80))
    country = db.Column(db.String(80))
    measurements = db.relationship('WaterMeasurement', backref='Watersource')

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def __init__(self, latitude, longitude, name, country):
        self.latitude = latitude
        self.longitude = longitude
        self.name = name
        self.country = country

    def __repr__(self):
        return "<WaterSource(name={self.name!r})>".format(self=self)

class WaterSourceSchema(SQLAlchemySchema):
    class Meta(SQLAlchemySchema.Meta):
        model = WaterSource
        sqla_session = db.session
    
    id = fields.Number(dump_only=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    name = fields.String(required=True)
    country = fields.String(required=True)
    
    @post_load
    def make_water_source(self, data, **kwargs):
        return WaterSource(**data)


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
    

# WaterMeasurement
class WaterMeasurement(db.Model):
    __tablename__ = 'WaterMeasurements'
    id = db.Column(db.Integer, primary_key=True)
    WaterSourceid = db.Column(db.Integer, db.ForeignKey("WaterSources.id"))
    ph = db.Column(db.Float)
    turbidity = db.Column(db.Float)
    conductivity = db.Column(db.Float)
    temperature = db.Column(db.Float)
    flow = db.Column(db.Float)
    datetime = db.Column(db.DateTime)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def __init__(self, WaterSourceid, ph, turbidity, conductivity, temperature, flow):
        self.WaterSourceid = WaterSourceid
        self.ph = ph
        self.turbidity = turbidity
        self.conductivity = conductivity
        self.temperature = temperature
        self.flow = flow
        self.datetime = datetime.datetime.utcnow()

    def __repr__(self):
        return "<WaterMeasurement(datetime={self.datetime!r})>".format(self=self)

class WaterMeasurementSchema(SQLAlchemySchema):
    class Meta(SQLAlchemySchema.Meta):
        model = WaterMeasurement
        sqla_session = db.session
    
    id = fields.Number(dump_only=True)
    WaterSourceid = fields.Number(dump_only=True)
    ph = fields.Float(required=True)
    turbidity = fields.Float(required=True)
    conductivity = fields.Float(required=True)
    temperature = fields.Float(required=True)
    flow = fields.Float(required=True)
    datetime = fields.DateTime(dump_only=True)

    @post_load
    def make_water_measurement(self, data, **kwargs):
        return WaterMeasurement(**data)

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

#
with app.app_context():
    db.create_all()

# Views
@app.route('/', methods=['GET'])
def home_page():
    return render_template('index.html')

@app.route('/map', methods=['GET'])
def map_page():
    return render_template('map.html')

@app.route('/earth', methods=['GET'])
def earth_page():
    return render_template('earth.html')

@app.route('/rank', methods=['GET'])
def rank_page():
    return render_template('rank.html')

@app.route('/about', methods=['GET'])
def about_page():
    return render_template('info.html')

if __name__ == '__main__':
    app.run()