# -*- coding: utf-8 -*-
{
    'name': 'ShareVault Custom',
    'version': '13.0.1.0.7',
    'category': 'Tools',
    'author': 'Wibtec',
    'website': 'www.wibtec.com',
    'summary': 'Custom changes in ShareVault',
    'description': """
- Hubspt fields
""",
    'depends': [
                'contacts',
                'mass_mailing'
                ],
    'data': [
            'data/country_data.xml',
            'views/partner_view.xml',
            ],
    'installable': True,
    'auto_install': False,
}
