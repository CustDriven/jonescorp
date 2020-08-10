# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError


class AccountInvoiceSend(models.TransientModel):
	_inherit = 'account.invoice.send'
	_description = 'Account Invoice Send'

	partner_cc_ids = fields.Many2many(
		'res.partner', 'account_invoice_send_cc_res_partner_rel',
		'wizard_id', 'partner_id', 'CC')
	partner_bcc_ids = fields.Many2many(
		'res.partner', 'account_invoice_send_bcc_res_partner_rel',
		'wizard_id', 'partner_id', 'BCC')
	cc_visible = fields.Boolean('Enable Email CC', readonly=True)
	bcc_visible = fields.Boolean('Enable Email BCC', readonly=True)

	@api.model
	def default_get(self, fields):
		result = super(AccountInvoiceSend, self).default_get(fields)
		default_cc_bcc = self.env.ref('email_cc_bcc_app.res_config_email_ccbcc_data1')
		if result:
			config_obj = self.env['res.config.settings'].search([], limit=1, order="id desc")
			if not config_obj:
				config_obj = default_cc_bcc
			result.update({
				'partner_cc_ids': [(6, 0, config_obj.partner_cc_ids.ids)],
				'partner_bcc_ids': [(6, 0, config_obj.partner_bcc_ids.ids)],
				'cc_visible' : config_obj.cc_visible,
				'bcc_visible' : config_obj.bcc_visible,
			})
			composer_id = self.env['mail.compose.message'].browse(result.get('composer_id'))
			composer_id.write({
				'partner_cc_ids': [(6, 0, config_obj.partner_cc_ids.ids)],
				'partner_bcc_ids': [(6, 0, config_obj.partner_bcc_ids.ids)],
				'cc_visible' : config_obj.cc_visible,
				'bcc_visible' : config_obj.bcc_visible,
			})
		return result


	def send_and_print_action(self):
		self.ensure_one()
		if self.composition_mode == 'mass_mail' and self.template_id:
			active_ids = self.env.context.get('active_ids', self.res_id)
			active_records = self.env[self.model].browse(active_ids)
			langs = active_records.mapped('partner_id.lang')
			default_lang = get_lang(self.env)

			for lang in (set(langs) or [default_lang]):
				active_ids_lang = active_records.filtered(lambda r: r.partner_id.lang == lang).ids
				self_lang = self.with_context(active_ids=active_ids_lang, lang=lang)	
				self_lang.onchange_template_id()
				self_lang._send_email()

		else:
			self._send_email()

		if self.is_print:
			return self._print_document()
		return {'type': 'ir.actions.act_window_close'}

	def _send_email(self):

		if self.is_email:
			self.composer_id.send_mail()
			if self.env.context.get('mark_invoice_as_sent'):
				self.mapped('invoice_ids').write({'invoice_sent': True})

