# -*- coding: utf-8 -*-
{
    'name': "cap_inspection_process",

    'summary': """
        Adds the Services, Locations and Windows module 
    """,

    'description': """
        Adds the Services, Locations and Windows module to Odoo to make the inspection process
    """,

    'author': "Captivea",
    'website': "http://www.captivea.com",
    
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale',  'project', 'stock', 'crm'],

    # 'data': [
    #  # 'security/ir.model.access.csv',
    #      'views/views.xml',
    #      #'views/templates.xml',
    # ],
    # # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}