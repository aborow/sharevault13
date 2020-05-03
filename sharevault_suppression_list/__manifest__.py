# -*- coding: utf-8 -*-
{
    'name': 'ShareVault - suppression list',
    'version': '13.0.1.0.0',
    'category': 'Tools',
    'author': 'Wibtec',
    'website': 'www.wibtec.com',
    'summary': 'Management of email suppression list',
    'description': """

""",
    'depends': [
                'sharevault',
                'mass_mailing',
                ],
    'data': [
            'security/ir.model.access.csv',
            'views/mailing_view.xml',
            ],
    'installable': True,
    'auto_install': False,
}
