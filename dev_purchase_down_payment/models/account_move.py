# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import models, api, _
import time


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.onchange('purchase_vendor_bill_id', 'purchase_id')
    def _onchange_purchase_auto_complete(self):
        ''' Load from either an old purchase order, either an old vendor bill.

        When setting a 'purchase.bill.union' in 'purchase_vendor_bill_id':
        * If it's a vendor bill, 'invoice_vendor_bill_id' is set and the loading is done by '_onchange_invoice_vendor_bill'.
        * If it's a purchase order, 'purchase_id' is set and this method will load lines.

        /!\ All this not-stored fields must be empty at the end of this function.
        '''
        if self.purchase_vendor_bill_id.vendor_bill_id:
            self.invoice_vendor_bill_id = self.purchase_vendor_bill_id.vendor_bill_id
            self._onchange_invoice_vendor_bill()
        elif self.purchase_vendor_bill_id.purchase_order_id:
            self.purchase_id = self.purchase_vendor_bill_id.purchase_order_id
        self.purchase_vendor_bill_id = False

        if not self.purchase_id:
            return

        # Copy partner.
        self.partner_id = self.purchase_id.partner_id
        self.fiscal_position_id = self.purchase_id.fiscal_position_id
        self.invoice_payment_term_id = self.purchase_id.payment_term_id
        self.currency_id = self.purchase_id.currency_id

        # Copy purchase lines.
        po_lines = self.purchase_id.order_line - self.line_ids.mapped('purchase_line_id')
        new_lines = self.env['account.move.line']
        if self.purchase_id.down_payment_by == 'dont_deduct_down_payment':
            for line in po_lines.filtered(lambda l: not l.display_type):
                new_line = new_lines.new(line._prepare_account_move_line(self))
                new_line.account_id = new_line._get_computed_account()
                new_line._onchange_price_subtotal()
                new_lines += new_line
        if self.purchase_id.down_payment_by == 'deduct_down_payment':
            for line in self.purchase_id.order_line:
                new_line = new_lines.new(line._prepare_account_move_line(self))
                new_line.account_id = new_line._get_computed_account()
                new_line._onchange_price_subtotal()
                new_lines += new_line
        if self.purchase_id.down_payment_by in ['fixed', 'percentage']:
            amount = self.purchase_id.amount
            if self.purchase_id.down_payment_by == 'percentage':
                amount = self.purchase_id.amount_total * self.purchase_id.amount / 100
            po_line_obj = self.env['purchase.order.line']
            ir_param = self.env['ir.config_parameter']
            product = ir_param.sudo().get_param('dev_purchase_down_payment.down_payment_product_id')
            if product:
                product_id = self.env['product.product'].browse(int(product))
            po_line = po_line_obj.create({'name': _('Advance: %s') % (time.strftime('%m %Y'),),
                                          'price_unit': amount,
                                          'product_qty': 0.0,
                                          'order_id': self.purchase_id.id,
                                          'product_uom': product_id.uom_id.id,
                                          'product_id': product_id.id,
                                          'date_planned': self.purchase_id.date_order,
                                          'is_down_payment': True
                                          })
            data = {'product_id': product_id.id or False,
                    'name': _('Advance Payment'),
                    'price_unit': amount,
                    'quantity': 1,
                    'purchase_line_id': po_line.id,
                    'move_id': self.id}
            new_line = new_lines.new(data)
            new_line.account_id = new_line._get_computed_account()
            new_line._onchange_price_subtotal()
            new_lines += new_line


        new_lines._onchange_mark_recompute_taxes()

        # Compute invoice_origin.
        origins = set(self.line_ids.mapped('purchase_line_id.order_id.name'))
        self.invoice_origin = ','.join(list(origins))

        # Compute ref.
        refs = set(self.line_ids.mapped('purchase_line_id.order_id.partner_ref'))
        refs = [ref for ref in refs if ref]
        self.ref = ','.join(refs)

        # Compute _invoice_payment_ref.
        if len(refs) == 1:
            self._invoice_payment_ref = refs[0]

        self.purchase_id = False
        self._onchange_currency()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
