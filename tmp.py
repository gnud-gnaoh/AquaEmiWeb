from flask import Flask, request, render_template, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemySchema
from flask_marshmallow import Marshmallow, post_load
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:bubudeptrai2006@localhost:3306/bucketlist'
app.secret_key = 'mmb'

db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

### Models

# WaterSource
class WaterSource(db.Model):
    __tablename__ = 'WaterSources'
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    name = db.Column(db.String(80))
    country = db.Column(db.String(80))

    def __repr__(self):
        return '<WaterSource %s>' % self.id

class WaterSourceSchema(ma.Schema):
    class Meta:
        fields = ("id", "latitude", "longitude", "name", "country")
        model = WaterSource

watersource_schema = WaterSourceSchema()
watersources_schema = WaterSourceSchema(many=True)

class WaterSourceListResource(Resource):
    def get(self):
        posts = WaterSource.query.all()
        return watersources_schema.dump(posts)

    def post(self):
        new_post = WaterSource(
            latitude=request.json['latitude'],
            longitude=request.json['longitude'],
            name=request.json['name'],
            country=request.json['country']
        )
        db.session.add(new_post)
        db.session.commit()
        return watersource_schema.dump(new_post)

    def patch(self, post_id):
        post = WaterSource.query.get_or_404(post_id)

        if 'latitude' in request.json:
            post.latitude = request.json['latitude']
        if 'longitude' in request.json:
            post.longitude = request.json['longitude']    
        if 'name' in request.json:
            post.name = request.json['name']
        if 'country' in request.json:
            post.country = request.json['country']

        db.session.commit()
        return watersource_schema.dump(post)
    
    def delete(self, post_id):
        post = WaterSource.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return '', 204

api.add_resource(WaterSourceListResource, '/watersources')

class WaterSourceResource(Resource):
    def get(self, watersource_id):
        post = WaterSource.query.get_or_404(watersource_id)
        return watersource_schema.dump(post)

api.add_resource(WaterSourceResource, '/watersources/<int:watersource_id>')

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

# watersource api
# @app.route('/watersource', methods=['GET'])
# def watersource_index():
#     get_watersources = WaterSource.query.all()
#     watersource_schema = WaterSourceSchema(many=True)
#     watersources = watersource_schema.dump(get_watersources)
#     return make_response(jsonify({"watersource": watersources}))

# @app.route('/watersource/<id>', methods=['GET'])
# def watersource_get_by_id(id):
#     get_watersource = WaterSource.query.get(id)
#     watersource_schema = WaterSourceSchema()
#     watersource = watersource_schema.dump(get_watersource)
#     return make_response(jsonify({"watersource": watersource}))

# @app.route('/watersource', methods=['POST'])
# def watersource_create():
#     data = request.get_json()
#     watersource_schema = WaterSourceSchema()
#     print(data)
#     watersource = watersource_schema.load(data, many=True)
#     print(type(watersource), watersource)
#     result = watersource_schema.dump(watersource.create())
#     return make_response(jsonify({"watersource": result}), 200)

# @app.route('/watersource/<id>', methods=['PUT'])
# def watersource_update_by_id(id):
#     data = request.get_json()
#     get_watersource = WaterSource.query.get(id)
#     if data.get('latitude'):
#         get_watersource.latitude = data['latitude']
#     if data.get('longitude'):
#         get_watersource.longitude = data['longitude']
#     if data.get('name'):
#         get_watersource.name = data['name']
#     if data.get('country'):
#         get_watersource.country = data['country']    
#     db.session.add(get_watersource)
#     db.session.commit()
#     watersource_schema = WaterSourceSchema(only=['id', 'latitude', 'longitude', 'name', 'country'])
#     watersource = watersource_schema.dump(get_watersource)
#     return make_response(jsonify({"watersource": watersource}))

# @app.route('/watersource/<id>', methods=['DELETE'])
# def watersource_delete_by_id(id):
#     get_watersource = WaterSource.query.get(id)
#     db.session.delete(get_watersource)
#     db.session.commit()
#     return make_response("", 204)

if __name__ == '__main__':
    app.run()