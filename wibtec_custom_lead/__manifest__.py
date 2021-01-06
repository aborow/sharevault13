#! -*- encoding: utf-8 -*-
{
    'name': "Wibtec Lead Customization",
    'version': '13.0.1.0.32',
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
                'odoo_salesforce_connector',
                'website_custom_pages',
                ],
    'data': [
            'data/crm_stage_data.xml',
            'data/base_automation_data.xml',
            'data/mail_data.xml',
            'wizards/sync_lead_view.xml',
            'views/res_partner_view.xml',
            'views/crm_lead_view.xml',
            'views/res_company_view.xml',
            ],
    'installable': True,
}
