# -*- coding: utf-8 -*-
{
    'name': 'ShareVault - industry tags',
    'version': '13.0.1.0.0',
    'category': 'Tools',
    'author': 'Wibtec',
    'website': 'www.wibtec.com',
    'summary': 'Management of industry-related tags',
    'description': """
This module actually changes the code in 'sharevault' in order to deal with
subindustries in a different way.
""",
    'depends': [
                'sharevault',
                ],
    'data': [
            'views/partner_view.xml',
            ],
    'installable': True,
    'auto_install': False,
}
