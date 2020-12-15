#! -*- encoding: utf-8 -*-
{
    'name': "Sharevault Website Notification",
    'version': '13.0.1.0.2',
    'author': 'Wibtec',
    'website': 'http://www.wibtec.com',
    'category': 'Leads',
    'summary': 'SV-206: Notifications on website visits',
    'depends': ['website_form', 'website'],
    'data': [
            'security/ir.model.access.csv',
            'data/base_automation_data.xml',
            'data/mail_data.xml',
            'views/website_track_view.xml',
            ],
    'installable': True,
}
