from marshmallow import Schema, fields


class Picture(Schema):
	id = fields.String(required=True)
	author = fields.String()
	camera = fields.String()
	tags = fields.String()
	cropped_picture = fields.String(required=True)
	full_picture = fields.String()
