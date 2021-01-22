# -*- coding: utf-8 -*-
{
    'name': 'ShareVault Custom',
    'version': '13.0.1.0.9',
    'category': 'Tools',
    'author': 'Wibtec',
    'website': 'www.wibtec.com',
    'summary': 'Custom changes in ShareVault',
    'description': """
- Hubspot fields
- Making mailings available in Contacts
- Making previous mailings available in mailing filter
""",
    'depends': [
                'contacts',
                'mass_mailing'
                ],
    'data': [
            'data/country_data.xml',
            'views/partner_view.xml',
            'views/mailing_view.xml',
            ],
    'installable': True,
    'auto_install': False,
}
