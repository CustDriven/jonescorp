# -*- coding: utf-8 -*-

from odoo import models, fields, api


class KsLeaderboardItem(models.Model):
    _name = 'ks_leaderboard.leaderboard.item'
    _description = 'Leaderboards Items'

    name = fields.Char(string="Name")
    ks_model_id = fields.Many2one("ir.model", string="Model", required=True,
                                  domain=[('access_ids', '!=', False), ('transient', '=', False),
                                          ('model', 'not ilike', 'base_import%'), ('model', 'not ilike', 'ir.%'),
                                          ('model', 'not ilike', 'web_editor.%'), ('model', 'not ilike', 'web_tour.%'),
                                          ('model', '!=', 'mail.thread'), ('model', 'not ilike', 'ks_it%'),
                                          ('model', 'not ilike', 'ks_lea%')])
    ks_leaderboard_id = fields.Many2one("ks_leaderboard.leaderboard", string="Leaderboard")
    # ks_image = fields.Binary(attachment=True, string="Image")

    # Filter Fields ----------------------------------------------
    ks_domain = fields.Char(string="Domain")
    ks_date_filter_field_id = fields.Many2one('ir.model.fields',
                                              domain="[('model_id','=',ks_model_id),'|',('ttype','=','date'),"
                                                     "('ttype','=','datetime')]",
                                              string="Date Filter Field")
    ks_date_filter_selection = fields.Selection([
        ('l_none', 'None (Leaderboard)'),
        ('l_day', 'Today'),
        ('t_week', 'This Week'),
        ('t_month', 'This Month'),
        ('t_quarter', 'This Quarter'),
        ('t_year', 'This Year'),
        ('n_day', 'Next Day'),
        ('n_week', 'Next Week'),
        ('n_month', 'Next Month'),
        ('n_quarter', 'Next Quarter'),
        ('n_year', 'Next Year'),
        ('ls_day', 'Last Day'),
        ('ls_week', 'Last Week'),
        ('ls_month', 'Last Month'),
        ('ls_quarter', 'Last Quarter'),
        ('ls_year', 'Last Year'),
        ('l_week', 'Last 7 days'),
        ('l_month', 'Last 30 days'),
        ('l_quarter', 'Last 90 days'),
        ('l_year', 'Last 365 days'),
        ('l_custom', 'Custom Filter'),
    ], string="Date Filter Selection", default="l_none", required=True)

    ks_item_start_date = fields.Datetime(string="Start Date")
    ks_item_end_date = fields.Datetime(string="End Date")

    ks_refresh_rate = fields.Selection(selection=[
        ('5', '5 min'),
        ('10', '10 min'),
        ('15', '15 min'),
        ('30', '30 min'),
        ('60', '1 hr'),
    ], default='60', required=True, string="Refresh Rate")

    ks_record_limit = fields.Integer(default=5, string="Limit")
    ks_ranking_order = fields.Selection([('ASC', 'Ascending'), ('DESC', 'Descending')],
                                        string="Ranking Order", required=True, default='DESC')

    ks_ranking_field_id = fields.Many2one('ir.model.fields', required=True,
                                          domain="[('model_id', '=', ks_model_id), ('name', '!=', 'id'),('store', '=', True), '|', '|', ('ttype', '=', 'integer'),('ttype', '=', 'float'), ('ttype', '=', 'monetary')]",
                                          string="Ranking Field")

    ks_group_by_field_id = fields.Many2one('ir.model.fields',
                                           domain="[('model_id', '=', ks_model_id), ('name', '!=', 'id'),('store', '=', True), ('ttype', '!=', 'binary'),('ttype', '!=', 'many2many'), ('ttype', '!=', 'one2many')]",
                                           string="Group By")
    ks_group_by_field_name = fields.Char(related='ks_group_by_field_id.relation', string="Group By Field Name")

    ks_item_image_field_id = fields.Many2one('ir.model.fields',
                                             domain="[('model_id', '=', ks_model_id), ('store', '=', True), ('ttype', '=', 'binary')]",
                                             string="Image Field")
    ks_item_image_relation_field_id = fields.Many2one('ir.model.fields',
                                                      domain=lambda self: [('model', '=',self.ks_group_by_field_name),('store', '=', True),('ttype', '=', 'binary')],
                                                      string="Relation Image Field")

    ks_model_name = fields.Char(related='ks_model_id.model', string="Model Name")

    ks_item_preview = fields.Char(string="Item Preview", store=True, default="Preview")  # for Item view purpose only

    ks_group_by_field_type = fields.Selection(string='Group By Field Type', related="ks_group_by_field_id.ttype",
                                              store=True)

    ks_group_by_date_selection = fields.Selection([
        ('day', 'Day'),
        ('week', 'Week'),
        ('month', 'Month'),
        ('quarter', 'Quarter'),
        ('year', 'Year'),
    ], string="Group By Date", default="day")

    ks_allow_grouping = fields.Boolean(string="Use Grouping", required=True, default=False)
    ks_gridstack_config = fields.Char(string="Gridstack Config", default=False,
                                      help="This Field store the Stringify Dict of Gridstack Item Configuration")

    # Display Related Fields (Attaching display in end to easily search display fields if needed)------------------
    ks_header_layout_display = fields.Selection([
        ('layout_1', 'Layout 1'),
        ('layout_2', 'Layout 2'),
        ('layout_3', 'Layout 3'),
        ('layout_4', 'Layout 4'),
        ('layout_5', 'Layout 5'),
    ], string="Header Layout", default="layout_1", required=True)

    ks_body_layout_display = fields.Selection([
        ('layout_1', 'Layout 1'),
        ('layout_2', 'Layout 2'),
        ('layout_3', 'Layout 3'),
        ('layout_4', 'Layout 4'),
        ('layout_5', 'Layout 5'),
    ], string="Body Layout", default="layout_1", required=True)

    ks_item_theme_display = fields.Selection([
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('red', 'Red'),
        ('white_black', 'White/Black'),
    ], string="Item Theme",
        default="blue")  # Cannot make this field required cause later may required to set false when custom color set

    ks_item_theme_gradient = fields.Boolean(string="Use Gradient", default=False)

    # Target Fields ------------------------------------------------------------
    # ks_target_type_selection = fields.Selection(string="Target Type")
    ks_target_enabled = fields.Boolean(string="Set Target")
    ks_target_value = fields.Float(string="Target Value", help="This value will be compared with each records rank value.")


    # @api.one
    @api.onchange('ks_model_id')
    def ks_model_change(self):
        return {'value': {
            'ks_ranking_field_id': False,
            'ks_domain': False,
            'ks_group_by_field_id': False,
            'ks_item_image_field_id': False,
            'ks_item_image_relation_field_id': False,
        }
        }

    @api.onchange('ks_allow_grouping', 'ks_group_by_field_id', 'ks_model_id')
    def _ks_image_item_domain(self):
        """
        Function mainly to handle dynamic domain change for image field
        :return: dict @containing image domains
        """
        return {
            'value': {'ks_item_image_field_id': False,
                      'ks_item_image_relation_field_id': False}
        }
