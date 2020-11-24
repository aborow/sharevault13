# -*- coding: utf-8 -*-
{
    'name': 'ShareVault Custom',
    'version': '13.0.1.0.2',
    'category': 'Tools',
    'author': 'Wibtec',
    'website': 'www.wibtec.com',
    'summary': 'Custom changes in ShareVault',
    'description': """
- Hubspt fields
- Keep website header fixed
""",
    'depends': [
                'contacts',
                'website',
                'web',
                ],
    'data': [
            'data/country_data.xml',
            'views/partner_view.xml',
            'views/website_templates.xml',
            ],
    'installable': True,
    'auto_install': False,
}
