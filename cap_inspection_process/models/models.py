# -*- coding: utf-8 -*-
import base64
from odoo import models, fields, api
from datetime import date

class Transfer(models.Model):
    _inherit = 'stock.picking'

    def print_barcode(self):
        datas = { 'ids': [self.id],}
        # return self.env['ir.actions.report'].search([('id','=',706)])[0].report_action([self.id], data=datas)
        # return self.env.ref('studio_customization.studio_report_docume_a8b80cba-44d2-4d4c-a834-a5e9e072854e').report_action([self.id], data=datas)
        context = self._context
        return {'type': 'ir.actions.report','report_name': 'studio_customization.studio_report_docume_a8b80cba-44d2-4d4c-a834-a5e9e072854','report_type':"qweb-pdf",'data': {'ids': [self.id]}}