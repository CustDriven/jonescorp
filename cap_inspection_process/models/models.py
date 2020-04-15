# -*- coding: utf-8 -*-
import base64
from odoo import models, fields, api
from datetime import date

class Transfer(models.Model):
    _inherit = 'stock.picking'

    def print_barcode(self):
        datas = { 'ids': [self.id],}
        return self.env['ir.actions.report'].search([('id','=',706)])[0].report_action([], data=datas)
