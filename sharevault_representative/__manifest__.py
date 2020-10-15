#! -*- encoding: utf-8 -*-
{
    'name': "ShareVault Representative",
    'version': '13.0.1.0.3',
    'author': 'Wibtec',
    'website': 'http://www.wibtec.com',
    'category': 'Extra tools',
    'summary': 'ShareVault Representative',
    'description': 'Added Menu For ShareVault Representative',
    'depends': [
        'sharevault',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/representative_view.xml',
        'views/sale_view.xml',
        'views/account_move_view.xml',
    ],
    'installable': True,
}
