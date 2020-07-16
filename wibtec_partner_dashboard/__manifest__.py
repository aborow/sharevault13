#! -*- encoding: utf-8 -*-
{
    'name': "Wibtec Partner Dashboard",
    'version': '13.0.1.0.0',
    'author': 'Wibtec',
    'website': 'http://www.wibtec.com',
    'category': 'Extra Tools',
    'summary': '',
    'description': """
Allows to select actions/views to show in a contact-related dashboard.

Use x_partner_id for any model that does not connect directly to res.partner
through partner_id field.

    """,
    'depends': ['base_setup', 'board', 'mail'],
    'data': [
            'data/action_data.xml',
            'data/field_data.xml',
            'views/res_partner_view.xml',
            'views/res_config_settings_view.xml'
            ],
    'installable': True,
}
