from odoo import fields, models,api
from datetime import date,datetime


class ProductProduct(models.Model):
	_inherit="product.template"

	commission = fields.Float(string="Commission",default=5)


