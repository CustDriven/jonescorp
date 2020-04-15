# -*- coding: utf-8 -*-
import base64
from odoo import models, fields, api
from datetime import date

class Transfer(models.Model):
    _inherit = 'stock.picking'

    def print_barcode(self):
        # datas = { 'ids': [self.id],}

        res = self.read()
        res = {'move_ids_without_package': self.move_ids_without_package}
        datas = {
            'ids': [self.id],
            'model': 'stock.picking',
            'form': res,
            'docs': [self.id]
            }
        # return self.env['ir.actions.report'].search([('id','=',706)])[0].report_action([self.id], data=datas)
        return self.env.ref('studio_customization.transfer_report_5dadae11-98a4-4a49-b45f-a14e1dc2d03b').report_action(67, data=datas)
        # context = self._context
        # [data] = self.read()
        # data['emp'] = self.env.context.get('active_ids', [])
        # employees = self.env['stock.picking'].browse(data['emp'])
        # res = {'move_ids_without_package': self.move_ids_without_package}
        # datas = {
        #     'ids': [self.id],
        #     'model': 'stock.picking',
        #     'form': res
        #     }

        # return {'type': 'ir.actions.report','report_name': 'studio_customization.studio_report_docume_a8b80cba-44d2-4d4c-a834-a5e9e072854','report_type':"qweb-pdf",'data': datas}

        # datas = {'ids': self.env.context.get('active_ids', [])}
        # res = self.read(['move_ids_without_package', 'id'])
        # res = res and res[0] or {}
        # res['move_ids_without_package'] = res['move_ids_without_package']
        # datas['form'] = res
        # return self.env.ref('studio_customization.transfer_report_5dadae11-98a4-4a49-b45f-a14e1dc2d03b').report_action([], data=datas)