import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow import fields, post_load
from math import cos, asin, sqrt, pi

db = SQLAlchemy()

# WaterSource
class WaterSource(db.Model):
    __tablename__ = 'WaterSources'
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    name = db.Column(db.String(300))
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
    DO = db.Column(db.Float) # dissolved oxygen
    BOD = db.Column(db.Float) # Biochemical oxygen demand
    datetime = db.Column(db.DateTime)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def __init__(self, WaterSourceid, ph, turbidity, conductivity, temperature, flow, DO, BOD):
        self.WaterSourceid = WaterSourceid
        self.ph = ph
        self.turbidity = turbidity
        self.conductivity = conductivity
        self.temperature = temperature
        self.flow = flow
        self.DO = DO
        self.BOD = BOD
        self.datetime = datetime.datetime.utcnow()

    def __repr__(self):
        return "<WaterMeasurement(datetime={self.datetime!r})>".format(self=self)

class WaterMeasurementSchema(SQLAlchemySchema):
    class Meta(SQLAlchemySchema.Meta):
        model = WaterMeasurement
        sqla_session = db.session
    
    id = fields.Number(dump_only=True)
    WaterSourceid = fields.Number(required=True)
    ph = fields.Float(required=True)
    turbidity = fields.Float(required=True)
    conductivity = fields.Float(required=True)
    temperature = fields.Float(required=True)
    flow = fields.Float(required=True)
    DO = fields.Float(required=True)
    BOD = fields.Float(required=True)
    datetime = fields.DateTime(dump_only=True)

    @post_load
    def make_water_measurement(self, data, **kwargs):
        return WaterMeasurement(**data)


# WaterMeasurementApp
def distance(lat1, lon1, lat2, lon2):
    r = 6371 # km
    p = pi / 180

    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 2 * r * asin(sqrt(a))

class WaterMeasurementApp(db.Model):
    __tablename__ = 'WaterMeasurementApps'
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    WaterSourceid = db.Column(db.Integer, db.ForeignKey("WaterSources.id"))
    turbidity = db.Column(db.Float)
    color = db.Column(db.String(20))
    datetime = db.Column(db.DateTime)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, latitude, longitude, turbidity, color):
        self.latitude = latitude
        self.longitude = longitude
        watersources = WaterSource.query.all()

        closest_watersource = watersources[0]
        for watersource in watersources:
            if distance(latitude, longitude, closest_watersource.latitude, closest_watersource.longitude) \
            > distance(latitude, longitude, watersource.latitude, watersource.longitude):
                closest_watersource = watersource
        
        self.WaterSourceid = closest_watersource.id
        self.turbidity = turbidity
        self.color = color
        self.datetime = datetime.datetime.utcnow()

    def __repr__(self):
        return "<WaterMeasurementApp(datetime={self.datetime!r})>".format(self=self)

class WaterMeasurementAppSchema(SQLAlchemySchema):
    class Meta(SQLAlchemySchema.Meta):
        model = WaterMeasurementApp
        sqla_session = db.session
    
    id = fields.Number(dump_only=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    WaterSourceid = fields.Number(dump_only=True)
    turbidity = fields.Float(required=True)
    color = fields.String(required=True)
    datetime = fields.DateTime(dump_only=True)

    @post_load
    def make_water_measurement_app(self, data, **kwargs):
        return WaterMeasurementApp(**data)