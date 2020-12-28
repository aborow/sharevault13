# -*- coding: utf-8 -*-
{
    'name': "Update Customers",

    'summary': """
        This Module is use to update Customers. """,

    'description': """
        SV-58 = Migrate Customer staging to staging2.
    """,

    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Contacts',
    'version': '13.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['contacts'],

    # always loaded
    'data': [
        'wizard/update_customers_view.xml',
    ],

    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}