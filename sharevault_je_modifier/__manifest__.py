#! -*- encoding: utf-8 -*-
{
    'name': "ShareVault JE Modifier",
    'version': '13.0.1.0.1',
    'author': 'Wibtec',
    'website': 'http://www.wibtec.com',
    'category': 'Accounting',
    'summary': 'ShareVault JE Modifier',
    'description': 'Added Historical Info Tab in Journal Entry View',
    'depends': [
        'sharevault_representative',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/import_je_views.xml',
        'views/account_move_view.xml',
    ],
    'installable': True,
}
