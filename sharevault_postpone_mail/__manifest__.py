# -*- coding: utf-8 -*-
{
    'name': 'ShareVault - postpone mail sending',
    'version': '13.0.1.0.6',
    'category': 'Tools',
    'author': 'Wibtec',
    'website': 'www.wibtec.com',
    'summary': 'Postpone mail sending (for mailings)',
    'description': """
On certain weekdays, mass emails should not be sent.
Mailings are automatically scheduled according to what is defined in settings.
""",
    'depends': [
                'mass_mailing',
                'base_automation'
                ],
    'data': [
            'data/base_automation_data.xml',
            'views/res_config_settings_views.xml'
            ],
    'installable': True,
    'auto_install': False,
}
