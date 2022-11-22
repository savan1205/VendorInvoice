from odoo import fields, models,api


class AccountMove(models.Model):
	_inherit="account.move"

	check_commission = fields.Boolean(string="Is Commission")




