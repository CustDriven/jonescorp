# -*- coding: utf-8 -*-
# Copyright 2014-2018 Akretion France
# @author: Alexis de Lattre <alexis@via.ecp.fr>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Base Phone',
    'version': '12.0.1.0.1',
    'category': 'Phone',
    'license': 'AGPL-3',
    'summary': 'Validate phone numbers',
    'author': "Akretion,Odoo Community Association (OCA)",
    'website': 'http://www.akretion.com/',
    'depends': ['base_setup','product.product'],
    'external_dependencies': {'python': ['phonenumbers']},
    'data': [
        ],
    'qweb': ['static/src/xml/phone.xml'],
    'images': [],
    'installable': True,
}
