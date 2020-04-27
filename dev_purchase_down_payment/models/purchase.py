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


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def get_purchase_total_invoices_amount(self):
        for purchase in self:
            payment = 0
            if purchase.invoice_ids:
                for bill in purchase.invoice_ids:
                    payment += bill.amount_total
            purchase.total_invoices_amount = payment

    def hide_create_bill_status(self):
        for purchase in self:
            if purchase.total_invoices_amount >= purchase.amount_total:
                purchase.hide_create_bill = True
            else:
                purchase.hide_create_bill = False

    total_invoices_amount = fields.Float(string='Advance Payment Amount', compute='get_purchase_total_invoices_amount')
    down_payment_by = fields.Selection(selection=[('dont_deduct_down_payment', 'Billable lines'),
                                                  ('deduct_down_payment', 'Billable lines (deduct advance payments)'),
                                                  ('percentage', 'Advance payment (percentage)'),
                                                  ('fixed', 'Advance payment (fixed amount)')],
                                       string='What do you want to bill?')
    amount = fields.Float(string='Amount')
    dp_journal_id = fields.Many2one('account.journal', string='Journal')
    hide_create_bill = fields.Boolean(string='Hide Create Bill', copy=False, compute='hide_create_bill_status')


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def _prepare_account_move_line(self, move):
        res = super(PurchaseOrderLine, self)._prepare_account_move_line(move)
        if self.order_id.down_payment_by == 'dont_deduct_down_payment':
            if self.is_down_payment:
                return {}
            else:
                res.update({'quantity': res.get('quantity')})
        if self.order_id.down_payment_by == 'deduct_down_payment':
            if self.is_down_payment:
                res.update({'quantity': -1})
            else:
                res.update({'quantity': res.get('quantity')})
        return res

    is_down_payment = fields.Boolean(string='Advance Payment')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
