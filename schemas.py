from marshmallow import Schema, fields


class Picture(Schema):
	id = fields.String(required=True)
	author = fields.String(required=True)
	camera = fields.String(required=True)
	tags = fields.String(required=True)
	cropped_picture = fields.String(required=True)
	full_picture = fields.String(required=True)
