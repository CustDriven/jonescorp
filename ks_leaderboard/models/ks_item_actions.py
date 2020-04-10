from odoo import fields, models, api


class ModelName (models.TransientModel):
    _name = 'ks_leaderboard.leaderboard.item_actions'
    _description = 'Item Actions Wizard'

    name = fields.Char()
    ks_lb_item_ids = fields.Many2many(comodel_name="ks_leaderboard.leaderboard.item", relation="ks_action_items_rel", column1="action_id", column2="item_id", string="Leaderboard Items")
    ks_action = fields.Selection([('move', 'Move'),
                                  ('duplicate', 'Duplicate'),
                                  ], string="Action")
    ks_lb_id = fields.Many2one("ks_leaderboard.leaderboard", string="Select Leaderboard")
    ks_lb_ids = fields.Many2many(comodel_name="ks_leaderboard.leaderboard", relation="ks_action_lb_rel", column1="action_id", column2="lb_id", string="Select Leaderboards")


    # Move or Copy item to another dashboard action

    def action_item_move_copy_action(self):
        ks_lb_item_ids = self.env['ks_leaderboard.leaderboard.item'].browse(self._context.get('active_ids', []))
        if self.ks_action == 'move':
            for item in ks_lb_item_ids:
                item.ks_leaderboard_id = self.ks_lb_id
        elif self.ks_action == 'duplicate':
            # Using sudo here to allow creating same item without any security error
            for lb_id in self.ks_lb_ids:
                for item in ks_lb_item_ids:
                    item.sudo().copy({'ks_leaderboard_id': lb_id.id})


