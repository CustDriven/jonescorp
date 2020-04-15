# Copyright 2016-2019 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, models


class Product(models.Model):
    _name = 'product.product'
    _inherit = ['product.product']

   
    def print_report_barcode(self):
    #   return self.env.ref('product.report_productbarcode').report_action(self)
      return {
            'type': 'ir.actions.report.xml', 
            'report_name':'product.report_productbarcode',
            'datas': {
                    'model':'account.voucher',
                    'id': self.id,
                    'ids': [self.id],
                    'report_type': 'webkit'
                },
            'nodestroy': True
            }
