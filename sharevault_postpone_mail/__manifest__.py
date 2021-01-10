# -*- coding: utf-8 -*-
{
    'name': 'ShareVault - postpone mail sending',
    'version': '13.0.1.0.5',
    'category': 'Tools',
    'author': 'Wibtec',
    'website': 'www.wibtec.com',
    'summary': 'Postpone mail sending (for mailings)',
    'description': """
On certain weekdays, emails should not be sent
""",
    'depends': [
                'mail',
                'base_automation'
                ],
    'data': [
            'data/base_automation_data.xml',
            'views/res_config_settings_views.xml'
            ],
    'installable': True,
    'auto_install': False,
}
