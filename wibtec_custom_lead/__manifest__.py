#! -*- encoding: utf-8 -*-
{
    'name': "Wibtec Lead Customization",
    'version': '13.0.1.0.16',
    'author': 'Wibtec',
    'website': 'http://www.wibtec.com',
    'category': 'Leads',
    'summary': 'SV-141: Lead Customization, SMS sending',
    'depends': [
                'base',
                'crm',
                'sms', 'mail',
                'base_automation',
                'website_crm_score',
                'utm',
                ],
    'data': [
            'data/crm_stage_data.xml',
            'data/base_automation_data.xml',
            'data/mail_data.xml',
            'views/crm_lead_view.xml',
            ],
    'installable': True,
}
