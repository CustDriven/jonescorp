# -*- coding: utf-8 -*-

from . import controllers
from . import models

from odoo.api import Environment, SUPERUSER_ID


def uninstall_hook(cr, registry):
    env = Environment(cr, SUPERUSER_ID, {})
    for rec in env['ks_leaderboard.leaderboard'].search([]):
        rec.ks_leaderboard_action_id.unlink()
        rec.ks_leaderboard_menu_id.unlink()