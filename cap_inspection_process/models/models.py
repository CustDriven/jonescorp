# -*- coding: utf-8 -*-
import base64
from odoo import models, fields, api
from datetime import date


import logging
_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = 'product.product'

    route_ids = fields.Many2many('stock.location.route', 'stock_route_variant', 'product_id', 'route_id', 'Routes', domain="[('product_selectable', '=', True)]", help="Depending on the modules installed, this will allow you to define the route of the product: whether it will be bought, manufactured, MTO/MTS,...")

class Transfer(models.Model):
    _inherit = 'stock.picking'                                  

    def print_barcode(self):
        return self.env.ref('studio_customization.transfer_report_5dadae11-98a4-4a49-b45f-a14e1dc2d03b').report_action(self)
        
    def print_picking(self):
        return self.env.ref('stock.action_report_picking').report_action(self)

class Lead2OpportunityPartner(models.TransientModel):

    _inherit = 'crm.lead2opportunity.partner'

    def action_apply(self):
        """ Convert lead to opportunity or merge lead and opportunity and open
            the freshly created opportunity view.
        """

        _logger.info("LAAAAAAAAAAAUNCHED !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        _logger.info(str(self.env.context))
        self.ensure_one()
        values = {
            'team_id': self.team_id.id,
        }

        if self.partner_id:
            values['partner_id'] = self.partner_id.id

        if self.name == 'merge':
            leads = self.with_context(active_test=False).opportunity_ids.merge_opportunity()
            if not leads.active:
                leads.write({
                    'active': True,
                    'activity_type_id': False,
                    'lost_reason': False,
                })
            if leads.type == "lead":
                values.update({'lead_ids': leads.ids, 'user_ids': [self.user_id.id]})
                self.with_context(active_ids=leads.ids)._convert_opportunity(values)
            elif not self._context.get('no_force_assignation') or not leads.user_id:
                values['user_id'] = self.user_id.id
                leads.write(values)
        else:
            leads = self.env['crm.lead'].browse(self._context.get('active_ids', []))
            values.update({'lead_ids': leads.ids, 'user_ids': [self.user_id.id]})
            self._convert_opportunity(values)
        if self.x_estimated_close_date and self.x_estimated_value and self.x_opp_type:
            leads.write({
                        'date_deadline': self.x_estimated_close_date,
                        'planned_revenue': self.x_estimated_value,
                        'x_opportunity_type': self.x_opp_type,
                        'stage_id': 1,
                    })
        return leads[0].redirect_lead_opportunity_view()