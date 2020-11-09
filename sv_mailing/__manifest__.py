#! -*- encoding: utf-8 -*-
{
    'name': "ShareVault Mailing Report",
    'version': '13.0.1.0.0',
    'author': 'Wibtec',
    'website': 'http://www.wibtec.com',
    'category': 'Mail',
    'summary': 'Mailing Report',
    'description': 'Report as per hubspot in odoo',
    'depends': [
        'mass_mailing', 'web'
    ],
    'data': [
        'report/mass_mailing_templates.xml',
    ],
    'external_dependencies': {
        'python': ['matplotlib'],
    },
    'installable': True,
}
