from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

#API Config
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
#-----------------------------------------------------------------------------------------------------------------------

#DataBase
class VesselModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(), nullable=False)

class EquipmentModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vessel_code = db.Column(db.Integer, db.ForeignKey('vessel_model.code'))
    name = db.Column(db.String, nullable=False)
    code = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    status = db.Column(db.Boolean, default=True)

#db.create_all()
#-----------------------------------------------------------------------------------------------------------------------

#Validate Data
#Vessel
vessel_args = reqparse.RequestParser()
vessel_args.add_argument("code", type=str, help="Code of the vessel is required", required=True)

#Equipment equipment_list_args
equipment_args = reqparse.RequestParser()
equipment_args.add_argument("code", type=str, help="Code of the equipment is required", required=True)

equipment_list_args = reqparse.RequestParser()
equipment_list_args.add_argument("vessel_code", type=str, help="vessel_code of the equipment is required",required=True)
equipment_list_args.add_argument("status", type=str, help="Status of the equipment is required",)

equipment_update_args = reqparse.RequestParser()
equipment_update_args.add_argument("code", type=str, help="Code of the equipment is required", required=True)
equipment_update_args.add_argument("name", type=str, help="Name of the equipment is required")
equipment_update_args.add_argument("location", type=str, help="Location of the equipment is required")
equipment_update_args.add_argument("status", type=str, help="Status of the equipment is required")

equipment_put_args = reqparse.RequestParser()
equipment_put_args.add_argument("vessel_code", type=str, help="Vessel_code of the equipment is required", required=True)
equipment_put_args.add_argument("code", type=str, help="Code of the equipment is required", required=True)
equipment_put_args.add_argument("name", type=str, help="Name of the equipment is required", required=True)
equipment_put_args.add_argument("location", type=str, help="Location of the equipment is required", required=True)

#-----------------------------------------------------------------------------------------------------------------------

#field
vessel_resource_fields = {
	'id': fields.Integer,
    'code': fields.String
}

equipment_resource_fields = {
	'id': fields.Integer,
    'name': fields.String,
    'code': fields.String,
    'vessel_code': fields.String,
    'location': fields.String,
    'status': fields.Boolean
}
#-----------------------------------------------------------------------------------------------------------------------

#Vessel
class Vessel(Resource):
	@marshal_with(vessel_resource_fields)
	def get(self):
		args = vessel_args.parse_args()
		result = VesselModel.query.filter_by(code=args['code']).first()
		if not result:
			abort(404, message="Could not find vessel with that code")
		return result

	@marshal_with(vessel_resource_fields)
	def post(self):
		args = vessel_args.parse_args()
		result = VesselModel.query.filter_by(code=args['code']).first()
		if result:
			abort(409, message="Vessel code taken...")

		vessel = VesselModel(code=args['code'])
		db.session.add(vessel)
		db.session.commit()
		return vessel, 201

	def delete(self):
		args = vessel_args.parse_args()
		result = VesselModel.query.filter_by(code=args['code']).first()
		if result:
			VesselModel.query.filter_by(code=args['code']).delete()
			db.session.commit()
		else:
			abort(404, message="Vessel doesn't exist, cannot delete")
		return '', 204
#-----------------------------------------------------------------------------------------------------------------------

#Equipmente
class Equipmente(Resource):
	@marshal_with(equipment_resource_fields)
	def get(self):
		args = equipment_args.parse_args()
		result = EquipmentModel.query.filter_by(code=args['code']).first()
		if not result:
			abort(404, message="Could not find equipmente with that code")
		return result

	@marshal_with(equipment_resource_fields)
	def post(self):
		args = equipment_put_args.parse_args()
		result = EquipmentModel.query.filter_by(code=args['code']).first()
		if result:
			abort(409, message="Equipmente code taken...")

		equipmente = EquipmentModel(vessel_code=args['vessel_code'], code=args['code'], name=args['name'], location=args['location'])
		db.session.add(equipmente)
		db.session.commit()
		return equipmente, 201

	@marshal_with(equipment_resource_fields)
	def put(self):
		args = equipment_update_args.parse_args()
		result = EquipmentModel.query.filter_by(code=args['code']).first()
		if not result:
			abort(404, message="Equipment doesn't exist, cannot update")

		if args['name']:
			result.name = args['name']
		if args['location']:
			result.location = args['location']
		if args['status']:
			result.status = args['status']

		db.session.commit()
		return result

	def delete(self):
		args = equipment_args.parse_args()
		result = EquipmentModel.query.filter_by(code=args['code']).first()
		if result:
			EquipmentModel.query.filter_by(code=args['code']).delete()
			db.session.commit()
		else:
			abort(404, message="Equipment doesn't exist, cannot delete")
		return '', 204
#-----------------------------------------------------------------------------------------------------------------------

#EquipmenteList
class EquipmenteList(Resource):
	@marshal_with(equipment_resource_fields)
	def post(self):
		args = equipment_list_args.parse_args()
		if args['status']:
			result = EquipmentModel.query.filter_by(vessel_code=args['vessel_code'],status=args['status']).all()
		else:
			result = EquipmentModel.query.filter_by(vessel_code=args['vessel_code']).all()
		if not result:
			abort(404, message="Could not find equipmente with that vessel_code or status")
		return result
#-----------------------------------------------------------------------------------------------------------------------
api.add_resource(Vessel, "/vessel")
api.add_resource(Equipmente, "/equipmente")
api.add_resource(EquipmenteList, "/equipmenteList")

if __name__ == "__main__":
	app.run(debug=True)