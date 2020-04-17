# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    down_payment_product_id = fields.Many2one('product.product', string='Product')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ir_param = self.env['ir.config_parameter'].sudo()
        res['down_payment_product_id'] = int(ir_param.get_param('dev_purchase_down_payment.down_payment_product_id', default=False))
        return res

    @api.model
    def set_values(self):
        ir_param = self.env['ir.config_parameter'].sudo()
        ir_param.set_param('dev_purchase_down_payment.down_payment_product_id', self.down_payment_product_id.id)
        super(ResConfigSettings, self).set_values()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: