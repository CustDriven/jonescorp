# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel): 
	_inherit = 'res.config.settings'

	allow_warehouse = fields.Boolean(string="Allow Warehouse in Sale Order Line", default=False)

	def set_values(self):
		res = super(ResConfigSettings, self).set_values()
		self.env['ir.config_parameter'].sudo().set_param('sale_order_line_by_warehouse_app.allow_warehouse', self.allow_warehouse)

	@api.model
	def get_values(self):
		res = super(ResConfigSettings, self).get_values()
		config_parameter = self.env['ir.config_parameter'].sudo()
		allow_warehouse = config_parameter.get_param('sale_order_line_by_warehouse_app.allow_warehouse')
		res.update(allow_warehouse=allow_warehouse)
		return res
