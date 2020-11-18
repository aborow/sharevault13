# -*- coding: utf-8 -*-
{
    'name': 'ShareVault - changes to contact import',
    'version': '13.0.1.0.1',
    'category': 'Tools',
    'author': 'Wibtec',
    'website': 'www.wibtec.com',
    'summary': 'Changes to contact import',
    'description': """

""",
    'depends': [
                'sharevault',
                'contacts',
                'base_import',
    ],
    'data': [
        'data/ir_sequence_data.xml',
        'data/data.xml',
        'view/partner_view.xml'
    ],
    'installable': True,
    'auto_install': False,
}
