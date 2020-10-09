#! -*- encoding: utf-8 -*-
{
    'name': "Wibtec Lead Customization",
    'version': '13.0.1.0.0',
    'author': 'Wibtec',
    'website': 'http://www.wibtec.com',
    'category': 'Leads',
    'summary': 'SV-141: Lead Customization',
    'depends': ['base', 'crm', ],
    'data': [
            'data/crm_stage_data.xml',
            'views/crm_lead_view.xml',
            ],
    'installable': True,
}
