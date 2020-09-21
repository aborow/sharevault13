# -*- coding: utf-8 -*-
{
    'name': "Weekly Customer Report",
    'summary': """
            This Module is used to print report in excel format with invoice data of customer""",
    'description': """
    """,
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Accounting',
    'version': '13.0.1.0.0',
    # any module necessary for this one to work correctly
    'depends': ['account', 'base', 'sharevault_invoice'],
    # always loaded
    'data': [
        'views/res_partner_view.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}