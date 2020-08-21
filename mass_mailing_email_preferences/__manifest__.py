#! -*- encoding: utf-8 -*-
{
    'name': "Mass mailing Email preferences",
    'version': '13.0.1.0.1',
    'author': 'Wibtec',
    'website': 'http://www.wibtec.com',
    'category': 'Extra Tools',
    'summary': 'Mass mailing Email preferences',
    'description': 'Added email preferences tab in contacts',
    'depends': [
        'mail',
        'base',
        'mass_mailing',
        'website',
    ],
    'data': [
        'views/unsubscribe_page.xml',
        'views/res_partner_view.xml',
    ],
    'installable': True,
}
