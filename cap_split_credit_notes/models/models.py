from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero


# class PaymentInvoiceLine(models.Model):
#     _name = 'payment.invoice.line'
    
#     payment_id = fields.Many2one('account.payment', string="Payment")
#     invoice_id = fields.Many2one('account.move', string="Invoice")
#     invoice = fields.Char(related='invoice_id.name', string="Invoice Number")
#     account_id = fields.Many2one(related="invoice_id.company_id.property_account_receivable_id", string="Account")
#     date = fields.Date(string='Invoice Date', compute='_get_invoice_data', store=True)
#     due_date = fields.Date(string='Due Date', compute='_get_invoice_data', store=True)
#     total_amount = fields.Float(string='Total Amount', compute='_get_invoice_data', store=True)
#     open_amount = fields.Float(string='Due Amount', compute='_get_invoice_data', store=True)
#     allocation = fields.Float(string='Allocation Amount')
#     discount = fields.Float(string='Discount Amount')
    
    # @api.depends('invoice_id')
    # def _get_invoice_data(self):
    #     for data in self:
    #         invoice_id = data.invoice_id
    #         data.date = invoice_id.date_invoice
    #         data.due_date = invoice_id.date_due
    #         data.total_amount = invoice_id.amount_total 
    #         data.open_amount = invoice_id.residual

class InvoiceCreditNoteLine(models.Model):
    _name = 'invoice.creditnote.line'

    invoice_id = fields.Many2one('account.move', string="Invoice")
    credit_note_id = fields.Many2one('account.move', string="Credit Note")
    # credit_note = fields.Char(related='credit_note_id.name', string="Credit Note Number")
    # account_id = fields.Many2one(related="credit_note_id..partner_id.property_account_receivable_id", string="Account")
    # date = fields.Date(string='Credit Note Date', compute='_get_credit_note_data', store=True)
    # due_date = fields.Date(string='Due Date', compute='_get_credit_note_data', store=True)
    # total_amount = fields.Float(string='Total Amount', compute='_get_credit_note_data', store=True)
    # open_amount = fields.Float(string='Due Amount', compute='_get_credit_note_data', store=True)
    # allocation = fields.Float(string='Allocation Amount')

    # @api.depends('credit_note_id')
    # def _get_credit_note_data(self):
    #     for data in self:
    #         credit_note_id = data.credit_note_id
    #         data.date = credit_note_id.date_invoice
    #         data.due_date = credit_note_id.date_due
    #         data.total_amount = credit_note_id.amount_total 
    #         data.open_amount = credit_note_id.residual

class CreditNoteInvoiceLine(models.Model):
    _name = 'creditnote.invoice.line'

    credit_note_id = fields.Many2one('account.move', string="Credit Note")
    invoice_id = fields.Many2one('account.move', string="Invoice")
    # invoice = fields.Char(related='invoice_id.name', string="Invoice Number")
    # account_id = fields.Many2one(related="invoice_id.company_id.partner_id.property_account_receivable_id", string="Account")
    # date = fields.Date(string='Invoice Date', compute='_get_invoice_data', store=True)
    # due_date = fields.Date(string='Due Date', compute='_get_invoice_data', store=True)
    # total_amount = fields.Float(string='Total Amount', compute='_get_invoice_data', store=True)
    # open_amount = fields.Float(string='Due Amount', compute='_get_invoice_data', store=True)
    # allocation = fields.Float(string='Allocation Amount')

    # @api.depends('invoice_id')
    # def _get_invoice_data(self):
    #     for data in self:
    #         invoice_id = data.invoice_id
    #         data.date = invoice_id.date_invoice
    #         data.due_date = invoice_id.date_due
    #         data.total_amount = invoice_id.amount_total 
    #         data.open_amount = invoice_id.residual

class InvoiceRegisteredPayment(models.Model):
    _name = 'account.invoice.payment.registered'

    # name = fields.Char(String="Name")
    # journal_name = fields.Char(String="Journal Name")
    # amount = fields.Float(String="Amount")
    # currency = fields.Char(String="Currency")
    # date = fields.Date(String="Payment Date")
    # payment_id = fields.Many2one('account.move.line', String="Payment")
    # move_id = fields.Many2one('account.move', String="Journal Entry")
    # ref = fields.Char(String="Payment Ref")
    invoice_id = fields.Many2one('account.move', String="Invoice")
    # # digits = [69, currency_id.decimal_places],
    # # position = currency_id.position,

class AccountInvoice(models.Model):
    _inherit = 'account.move'

    credit_note_lines = fields.One2many('invoice.creditnote.line', 'invoice_id', string="Credit Note Lines")
    invoice_lines = fields.One2many('creditnote.invoice.line', 'credit_note_id', string="Invoice Lines")
    registered_payments = fields.One2many('account.invoice.payment.registered', 'invoice_id', String="Payments Registered")
    # , compute="_get_payments_registered_in_invoice", store=True

    # def update_invoice_and_credit_note_lines(self):
    #     for inv in self.credit_note_lines:
    #         inv.open_amount = inv.invoice_id.residual
    #     for inv in self.invoice_lines:
    #         inv.open_amount = inv.credit_note_id.residual 
    #     self.onchange_partner_id()
        
    # @api.onchange('partner_type')
    # def _onchange_partner_type(self):
    #     # Set partner_id domain
    #     if self.partner_type:
    #         if not self.env.context.get('default_invoice_ids'):
    #             self.partner_id = False
    #         return {'domain': {'partner_id': [(self.partner_type, '=', True)]}}

    # @api.onchange('partner_id', 'currency_id')
    # def onchange_partner_id(self):
    #     if self.partner_id:
    #         vals = {}
    #         invoice_lines = [(6, 0, [])]
    #         credit_note_lines = [(6, 0, [])]
    #         invoice_ids = []
    #         credit_note_ids = []
    #         if self.type == 'out_invoice':
    #             credit_note_ids = self.env['account.move'].search([('partner_id', 'in', [self.partner_id.id]),('state', '=','open'),('type','=', 'out_refund'),('currency_id', '=', self.currency_id.id)])
    #         if self.type == 'out_refund':
    #             invoice_ids = self.env['account.move'].search([('partner_id', 'in', [self.partner_id.id]),('state', '=','open'),('type','=', 'out_invoice'),('currency_id', '=', self.currency_id.id)])
    #         # IMPLEMENT FOR VENDOR BILLS
    #         # if self.payment_type == 'inbound' and self.partner_type == 'customer':
    #         #     invoice_ids = self.env['account.invoice'].search([('partner_id', 'in', [self.partner_id.id]),
    #         #                                                       ('state', '=','open'),
    #         #                                                       ('type','=', 'out_invoice'),
    #         #                                                       ('currency_id', '=', self.currency_id.id)])
    #         # if self.payment_type == 'outbound' and self.partner_type == 'customer':
    #         #     invoice_ids = self.env['account.invoice'].search([('partner_id', 'in', [self.partner_id.id]),
    #         #                                                       ('state', '=','open'),
    #         #                                                       ('type','=', 'out_refund'),
    #         #                                                       ('currency_id', '=', self.currency_id.id)])

    #         for inv in credit_note_ids[::-1]:
    #             vals = {'invoice_id': self.id, 'credit_note_id': inv.id}
    #             credit_note_lines.append((0, 0, vals))

    #         for inv in invoice_ids[::-1]:
    #             vals = {'credit_note_id': self.id, 'invoice_id': inv.id}
    #             invoice_lines.append((0, 0, vals))

    #         self.invoice_lines = invoice_lines
    #         self.credit_note_lines = credit_note_lines
    #         # self.onchnage_amount()
        
    # def register_new_payment(self):
    #     if self.type == 'out_invoice':
    #         invoice = self
    #         amt = 0
    #         for cn in self.credit_note_lines:
    #             # if cn.allocation <= 0:
    #             #     self['credit_note_lines'] = [(3, cn.id)]
    #             #     cn.unlink()
    #             if round(cn.allocation, 2) > round(cn.open_amount, 2):
    #                 raise ValidationError(("Allocated amount for credit note " + str(cn.credit_note) + " is higher than the due amount. Due amount is equal to " + str(round(cn.open_amount, 2)) + " and allocated amount is equal to %s") %(round(cn.allocation, 2)))
    #             else:
    #                 amt += cn.allocation
    #         if round(amt, 2) > round(self.residual, 2):
    #             raise ValidationError(("Total allocated amount is higher than Invoice due amount. Invoice due amount is equal to " + str(round(self.residual, 2)) + " and Total allocated amount is equal to %s") %(round(amt, 2)))
    #         else:
    #             for cn in self.credit_note_lines:
    #                 if cn.allocation > 0:
    #                     p_data = {'account_id': self.account_id.id, 'partner_id': self.partner_id.id, 'credit': 0, 'invoice_id': cn.credit_note_id.id, 'move_id': cn.credit_note_id.move_id.id}
    #                     move_line = False
    #                     for line in cn.credit_note_id.move_id.line_ids:
    #                         if line.account_id.id == self.account_id.id and line.reconciled == False and line.credit >= cn.allocation:
    #                             move_line = line
    #                             break
    #                     if move_line:
    #                         move = cn.credit_note_id.move_id
    #                         move.button_cancel()

    #                         payment_line = self.env['account.move.line'].create(p_data)
    #                         self.env.cr.commit()

                            
                            
    #                         move_line.with_context(check_move_validity=False).write({'credit': move_line.credit - cn.allocation})
    #                         payment_line.with_context(check_move_validity=False).write({'credit': cn.allocation})

    #                         self.env.cr.commit()

    #                         move.action_post()

    #                         self['payment_move_line_ids'] = [(4, payment_line.id)]
    #                         self.env.cr.commit()
                            
    #                         for p in invoice.payment_move_line_ids:
    #                             if p.id == payment_line.id:
    #                                 invoice.register_payment(p)
    #                         self.env.cr.commit()
    #                     else:
    #                         unreconciled_amt = 0
    #                         for line in cn.credit_note_id.move_id.line_ids:
    #                             if line.account_id.id == self.account_id.id and line.reconciled == False:
    #                                 unreconciled_amt += line.credit
    #                         if unreconciled_amt >= cn.allocation:
    #                             move = cn.credit_note_id.move_id
    #                             move.button_cancel()

    #                             payment_line = self.env['account.move.line'].create(p_data)
    #                             self.env.cr.commit()
    #                             amt_left = cn.allocation
    #                             for line in cn.credit_note_id.move_id.line_ids:
    #                                 if line.account_id.id == self.account_id.id and line.reconciled == False:
    #                                     if amt_left <= 0:
    #                                         break
    #                                     else:
    #                                         if amt_left <= line.credit:
    #                                             cred = line.credit
    #                                             line.with_context(check_move_validity=False).write({'credit': cred - amt_left})
    #                                             amt_left -= cred
    #                                         else:
    #                                             cred = line.credit
    #                                             line.with_context(check_move_validity=False).write({'credit': 0})
    #                                             amt_left -= cred
    #                             payment_line.with_context(check_move_validity=False).write({'credit': cn.allocation})
    #                             self.env.cr.commit()
    #                             move.action_post()

    #                             self['payment_move_line_ids'] = [(4, payment_line.id)]
    #                             self.env.cr.commit()
                                
    #                             for p in invoice.payment_move_line_ids:
    #                                 if p.id == payment_line.id:
    #                                     invoice.register_payment(p)
    #                             self.env.cr.commit()
    #                         else:
    #                             raise ValidationError(("Total allocated amount and Invoice due amount are not equal. Invoice due amount is equal to " + str(round(self.residual, 2)) + " and Total allocated amount is equal to %s") %(str(round(amt, 2))))         
                        
    #                     move = cn.credit_note_id.move_id
    #                     move.button_cancel()
    #                     for line in cn.credit_note_id.move_id.line_ids:
    #                         if line.account_id.id == self.account_id.id and line.reconciled == False and line.credit == 0 and line.debit == 0:
    #                             line.unlink()
    #                     move.action_post()

    #     if self.type == 'out_refund':
    #         credit_note = self
    #         amt = 0
    #         for inv in self.invoice_lines:
    #             if round(inv.allocation, 2) > round(inv.open_amount, 2):
    #                 raise ValidationError(("Allocated amount for Invoice " + str(inv.invoice) + " is higher than the due amount. Due amount is equal to " + str(round(inv.open_amount, 2)) + " and allocated amount is equal to %s") %(round(inv.allocation, 2)))
    #             else:
    #                 amt += inv.allocation
    #         if round(amt, 2) > round(self.residual, 2):
    #             raise ValidationError(("Total allocated amount is higher than Credit Note due amount. Credit Note due amount is equal to " + str(round(self.residual, 2)) + " and Total allocated amount is equal to %s") %(round(amt, 2)))
    #         else:
    #             for inv in self.invoice_lines:
    #                 if inv.allocation > 0:
    #                     p_data = {'account_id': inv.invoice_id.company_id.partner_id.property_account_receivable_id.account_id.id, 'partner_id': self.partner_id.id, 'credit': 0, 'invoice_id': self.id, 'move_id': self.move_id.id}
    #                     move_line = False
    #                     for line in self.move_id.line_ids:
    #                         if line.account_id.id == inv.invoice_id.company_id.partner_id.property_account_receivable_id.account_id.id and line.reconciled == False and line.credit >= inv.allocation:
    #                             move_line = line
    #                             break
    #                     if move_line:
    #                         move = self.move_id
    #                         move.button_cancel()

    #                         payment_line = self.env['account.move.line'].create(p_data)
    #                         self.env.cr.commit()

    #                         move_line.with_context(check_move_validity=False).write({'credit': move_line.credit - inv.allocation})
    #                         payment_line.with_context(check_move_validity=False).write({'credit': inv.allocation})
    #                         self.env.cr.commit()

    #                         move.action_post()

    #                         inv.invoice_id['payment_move_line_ids'] = [(4, payment_line.id)]
    #                         self.env.cr.commit()
                            
    #                         for p in inv.invoice_id.payment_move_line_ids:
    #                             if p.id == payment_line.id:
    #                                 inv.invoice_id.register_payment(p)
    #                         self.env.cr.commit()
    #                     else:
    #                         unreconciled_amt = 0
    #                         for line in self.move_id.line_ids:
    #                             if line.account_id.id == inv.invoice_id.account_id.id and line.reconciled == False:
    #                                 unreconciled_amt += line.credit
    #                         if unreconciled_amt >= inv.allocation:
    #                             move = inv.invoice_id.move_id
    #                             move.button_cancel()

    #                             payment_line = self.env['account.move.line'].create(p_data)
    #                             self.env.cr.commit()
    #                             amt_left = inv.allocation
    #                             for line in self.move_id.line_ids:
    #                                 if line.account_id.id == inv.invoice_id.account_id.id and line.reconciled == False:
    #                                     if amt_left <= 0:
    #                                         break
    #                                     else:
    #                                         if amt_left <= line.credit:
    #                                             cred = line.credit
    #                                             line.with_context(check_move_validity=False).write({'credit': cred - amt_left})
    #                                             amt_left -= cred
    #                                         else:
    #                                             cred = line.credit
    #                                             line.with_context(check_move_validity=False).write({'credit': 0})
    #                                             amt_left -= cred
    #                             payment_line.with_context(check_move_validity=False).write({'credit': inv.allocation})
    #                             self.env.cr.commit()
    #                             move.action_post()

    #                             inv.invoice_id['payment_move_line_ids'] = [(4, payment_line.id)]
    #                             self.env.cr.commit()
                                
    #                             for p in inv.invoice_id.payment_move_line_ids:
    #                                 if p.id == payment_line.id:
    #                                     inv.invoice_id.register_payment(p)
    #                             self.env.cr.commit()
    #                         else:
    #                             raise ValidationError(("Total allocated amount and Invoice due amount are not equal. Invoice due amount is equal to " + str(round(self.residual, 2)) + " and Total allocated amount is equal to %s") %(str(round(amt, 2))))         
                        
    #                     move = self.move_id
    #                     move.button_cancel()
    #                     for line in self.move_id.line_ids:
    #                         if line.account_id.id == inv.invoice_id.account_id.id and line.reconciled == False and line.credit == 0 and line.debit == 0:
    #                             line.unlink()
    #                     move.action_post()
    #     self.update_invoice_and_credit_note_lines()  



    # # @api.onchange('payment_type')
    # # def _onchange_payment_type(self):
    # #     if self.payment_type == 'transfer':
    # #         self.invoice_lines = [(6, 0, [])]
            
    # #     if not self.invoice_ids:
    # #         # Set default partner type for the payment type
    # #         if self.payment_type == 'inbound':
    # #             self.partner_type = 'customer'
    # #         elif self.payment_type == 'outbound':
    # #             self.partner_type = 'supplier'
    # #     # Set payment method domain
    # #     res = self._onchange_journal()
    # #     if not res.get('domain', {}):
    # #         res['domain'] = {}
    # #     res['domain']['journal_id'] = self.payment_type == 'inbound' and [('at_least_one_inbound', '=', True)] or [('at_least_one_outbound', '=', True)]
    # #     res['domain']['journal_id'].append(('type', 'in', ('bank', 'cash')))
    # #     return res
    
    # # @api.onchange('amount')
    # # def onchnage_amount(self):
    # #     total = 0.0
    # #     remain = self.amount
    # #     for line in self.invoice_lines:
    # #         if line.open_amount <= remain:
    # #             line.allocation = line.open_amount
    # #             remain -= line.allocation
    # #         else:
    # #             line.allocation = remain
    # #             remain -= line.allocation
    # #         total += line.allocation

    # @api.depends('residual')
    # @api.depends('payment_move_line_ids.amount_residual')
    # def _get_payments_registered_in_invoice(self):
    #     for s in self:
    #         if s.payment_move_line_ids:
    #             for pa in s.registered_payments:
    #                 pa.unlink()
    #             # info = {'title': _('Less Payment'), 'outstanding': False, 'content': []}
    #             payments_registered = []
    #             currency_id = s.currency_id
    #             for payment in s.payment_move_line_ids:
    #                 payment_currency_id = False
    #                 if s.type in ('out_invoice', 'in_refund'):
    #                     amount = sum([p.amount for p in payment.matched_debit_ids if p.debit_move_id in s.move_id.line_ids])
    #                     amount_currency = sum([p.amount_currency for p in payment.matched_debit_ids if p.debit_move_id in s.move_id.line_ids])
    #                     if payment.matched_debit_ids:
    #                         payment_currency_id = all([p.currency_id == payment.matched_debit_ids[0].currency_id for p in payment.matched_debit_ids]) and payment.matched_debit_ids[0].currency_id or False
    #                 elif s.type in ('in_invoice', 'out_refund'):
    #                     amount = sum([p.amount for p in payment.matched_credit_ids if p.credit_move_id in s.move_id.line_ids])
    #                     amount_currency = sum([p.amount_currency for p in payment.matched_credit_ids if p.credit_move_id in s.move_id.line_ids])
    #                     if payment.matched_credit_ids:
    #                         payment_currency_id = all([p.currency_id == payment.matched_credit_ids[0].currency_id for p in payment.matched_credit_ids]) and payment.matched_credit_ids[0].currency_id or False
    #                 # get the payment value in invoice currency
    #                 if payment_currency_id and payment_currency_id == s.currency_id:
    #                     amount_to_show = amount_currency
    #                 else:
    #                     # amount_to_show = payment.company_id.currency_id.with_context(date=payment.date).compute(amount, s.currency_id)
    #                     amount_to_show = amount
    #                 if float_is_zero(amount_to_show, precision_rounding=s.currency_id.rounding):
    #                     continue
    #                 payment_ref = payment.move_id.name
    #                 if payment.move_id.ref:
    #                     payment_ref += ' (' + payment.move_id.ref + ')'

    #                 payment_data = ({
    #                     'name': payment.name,
    #                     'journal_name': payment.journal_id.name,
    #                     'amount': amount_to_show,
    #                     'currency': currency_id.symbol,
    #                     'date': payment.date,
    #                     'payment_id': payment.id,
    #                     'move_id': payment.move_id.id,
    #                     'invoice_id': s.id,
    #                     'ref': payment_ref,
    #                 })

    #                 p = self.env['account.invoice.payment.registered'].create(payment_data)
    #                 self.env.cr.commit()

    #             # payments_registered.append(p.id)
    #         # self.registered_payments = [(6, 0, payments_registered)]