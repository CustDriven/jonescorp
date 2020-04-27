# -*- coding: utf-8 -*-
import base64
from odoo import models, fields, api
from datetime import date

class Transfer(models.Model):
    _inherit = 'stock.picking'                                  

    def print_barcode(self):
        return self.env.ref('studio_customization.transfer_report_5dadae11-98a4-4a49-b45f-a14e1dc2d03b').report_action(self)