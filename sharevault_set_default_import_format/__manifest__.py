# -*- coding: utf-8 -*-
{
    'name': "Set Default Import Format",

    'summary': """
        Make UTF-8 the default import format for Sharevault and Contact Imports. """,

    'description': """
        SV-101 = Make UTF-8 the default import format for Sharevault and Contact Imports.
    """,

    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Contacts',
    'version': '13.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base_import'],

    'data': [
        'views/assets.xml',
    ],

    # always loaded
    # 'data': [
    #     'wizard/update_customers_view.xml',
    # ],

    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}