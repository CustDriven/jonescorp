# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class KsLeaderBoard(models.Model):
    _name = 'ks_leaderboard.leaderboard'

    name = fields.Char(string="Leaderboard Name", required=True)
    ks_leaderboard_item_ids = fields.One2many('ks_leaderboard.leaderboard.item', 'ks_leaderboard_id',
                                              string='Leaderboard Items')
    ks_leaderboard_menu_name = fields.Char(string="Menu Name", required=True)
    ks_leaderboard_top_menu_id = fields.Many2one('ir.ui.menu', domain="[('parent_id','=',False)]",
                                                 string="Show Under Menu", required=True)
    ks_leaderboard_menu_priority = fields.Integer(string="Menu Priority", required=True, default=50)
    ks_leaderboard_active = fields.Boolean(string="Active", default=True)
    ks_leaderboard_group_access = fields.Many2many('res.groups', string="Group Access")

    ks_leaderboard_menu_id = fields.Many2one('ir.ui.menu', string="Leaderboard Menu Id")
    ks_leaderboard_action_id = fields.Many2one('ir.actions.act_window', string="Web Server Action Id")

    ks_leaderboard_default_template = fields.Many2one('ks_leaderboard.leaderboard.default_templates',
                                                      default=lambda self: self.env.ref('ks_leaderboard.ks_lb_blank',
                                                                                        False),
                                                      store=True,
                                                      string="Leaderboard Template")

    @api.model
    def create(self, vals):
        record = super(KsLeaderBoard, self).create(vals)

        action_vals = {
            'name': vals['ks_leaderboard_menu_name'] + " Action Id:" + str(record.id),
            'res_model': 'ks_leaderboard.leaderboard',
            'view_mode': 'ks_leaderboard',
            'res_id': record.id,
        }
        record.ks_leaderboard_action_id = self.env['ir.actions.act_window'].sudo().create(action_vals)

        record.ks_leaderboard_menu_id = self.env['ir.ui.menu'].sudo().create({
            'name': vals['ks_leaderboard_menu_name'],
            'active': vals.get('ks_leaderboard_active', True),
            'parent_id': vals['ks_leaderboard_top_menu_id'],
            'action': 'ir.actions.act_window,%d' % (record.ks_leaderboard_action_id.id,),
            'groups_id': vals.get('ks_leaderboard_group_access', False),
            'sequence': vals.get('ks_leaderboard_menu_priority', 50)
        })

        if record.ks_leaderboard_default_template and record.ks_leaderboard_default_template.ks_lb_item_count:
            for ks_lb_item in record.ks_leaderboard_default_template.ks_lb_item_ids:
                ks_lb_item.copy({'ks_leaderboard_id': record.id})

        return record


    def write(self, vals):
        record = super(KsLeaderBoard, self).write(vals)
        for rec in self:
            if 'ks_leaderboard_menu_name' in vals:
                rec.ks_leaderboard_menu_id.sudo().name = vals['ks_leaderboard_menu_name']
            if 'ks_leaderboard_group_access' in vals:
                rec.ks_leaderboard_menu_id.sudo().groups_id = vals['ks_leaderboard_group_access']
            if 'ks_leaderboard_active' in vals and rec.ks_leaderboard_menu_id:
                rec.ks_leaderboard_menu_id.sudo().active = vals['ks_leaderboard_active']

            if 'ks_leaderboard_top_menu_id' in vals:
                rec.ks_leaderboard_menu_id.write(
                    {'parent_id': vals['ks_leaderboard_top_menu_id']}
                )

            if 'ks_leaderboard_menu_priority' in vals:
                rec.ks_leaderboard_menu_id.sudo().sequence = vals['ks_leaderboard_menu_priority']

        return record


    def unlink(self):
        for rec in self:
            rec.ks_leaderboard_action_id.sudo().unlink()
            rec.ks_leaderboard_menu_id.sudo().unlink()
            rec.ks_leaderboard_item_ids.unlink()
        res = super(KsLeaderBoard, self).unlink()
        return res

    def ks_view_items_view(self):
        self.ensure_one()
        return {
            'name': _("Leaderboard Items"),
            'res_model': 'ks_leaderboard.leaderboard.item',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'views': [(False, 'tree'), (False, 'form')],
            'type': 'ir.actions.act_window',
            'domain': [('ks_leaderboard_id', '!=', False)],
            'search_view_id': self.env.ref('ks_leaderboard.ks_lb_item_search_view').id,
            'context': {
                    'search_default_ks_leaderboard_id': self.id,
                    'group_by': 'ks_leaderboard_id',
            },
            'help': _('''<p class="o_view_nocontent_smiling_face">
                                        You can find all items related to Leaderboard Here.</p>
                                    '''),
        }


class KsView(models.Model):
    _inherit = 'ir.ui.view'

    type = fields.Selection(selection_add=[('ks_leaderboard', 'Leaderboard')])


class KsLeaderBoardTemplates(models.Model):
    _name = 'ks_leaderboard.leaderboard.default_templates'

    name = fields.Char(string="Template Name")
    ks_lb_item_count = fields.Integer(string="Leaderboard Item Count")
    ks_lb_item_ids = fields.Many2many('ks_leaderboard.leaderboard.item', 'ks_leaderboard_template_item_rel',string="Leaderboard Items" )

