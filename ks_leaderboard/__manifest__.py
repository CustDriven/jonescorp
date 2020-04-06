# -*- coding: utf-8 -*-
{
    'name': "Leaderboard Ninja",

    'summary': """
        Leaderboard module offers a clear visual representation of your valuable module data in form of robust cards on a  Leaderboard
        """,

    'description': """
        Best Leader Board Apps
        Leader Board Apps
        Ranking Leader Board Apps
        Sales Order Leader Board Apps
        Product Leader Board Apps
        Inventory Leader Board
        POS Leader Board Apps
        Employee Leader Boards
        Enterprise Leader Boards
        Top Product Leader Boards
        Top Sale Leader Boards
        Odoo Leader Board Apps
        Top Ranking Leader Board
        Score Leader Board
        Bulletin Leader Board 
        Ranking System
        Points System
        Selling System
        Purchase System
        Company Leader Board
        Ranking Management Apps
        Ranking List Apps
        Rank Order List
        Odoo Ranking Board Apps
        Performance Leader Board Apps
        Employee Performance Leader Board
        Sale Performance Leader Board
        Best POS Leader BoardBest Leader Board Apps
        Leader Board Apps
        Ranking Leader Board Apps
        Sales Order Leader Board Apps
        Product Leader Board Apps
        Inventory Leader Board
        POS Leader Board Apps
        Employee Leader Boards
        Enterprise Leader Boards
        Top Product Leader Boards
        Top Sale Leader Boards
        Odoo Leader Board Apps
        Top Ranking Leader Board
        Score Leader Board
        Bulletin Leader Board 
        Ranking System
        Points System
        Selling System
        Purchase System
        Company Leader Board
        Ranking Management Apps
        Ranking List Apps
        Rank Order List
        Odoo Ranking Board Apps
        Performance Leader Board Apps
        Employee Performance Leader Board
        Sale Performance Leader Board
        Best POS Leader Board
    """,


    'author': "Ksolves India Pvt. Ltd.",
    'license': 'OPL-1',
    'currency': 'EUR',
    'price': 99.0,
    'website': "https://www.ksolves.com",
    'maintainer': 'Ksolves India Pvt. Ltd.',
    'category': 'Tools',
    'version': '13.0.1.1.1',
    'support': 'sales@ksolves.com',
    'images': ['static/description/banner_version_2.gif'],
    'live_test_url': 'https://leaderboard.kappso.com/web/demo_login',
    # any module necessary for this one to work correctly
    'depends': ['base','web'],

    # always loaded
    'data': [
        'data/ks_default_data.xml',
        'security/ir.model.access.csv',
        'security/ks_security_groups.xml',
        'views/ks_assets_backend.xml',
        'views/ks_leaderboard_views.xml',
        'views/ks_item_views.xml',
        'views/ks_item_action_views.xml',
    ],

    'qweb': [
        'static/src/xml/ks_cards.xml',
        'static/src/xml/ks_items_header.xml',
        'static/src/xml/ks_items.xml',
        'static/src/xml/ks_leaderboard.xml',
    ],

    'uninstall_hook': 'uninstall_hook',
}
