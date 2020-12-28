#! -*- encoding: utf-8 -*-
{
    'name': "Salesforce Connector",
    'version': '13.0.1.0.0',
    'author': 'Wibtec',
    'website': 'http://www.wibtec.com',
    'category': 'Leads',
    'summary': 'SV-172: Lifecycle Action - 40+, Subscriber --> marketing qualified lead, add lead to salesforce',
    'depends': [
                'base',
                'crm'
                ],
    'data': [
            'wizards/message_view.xml',
            'views/res_company_view.xml',
            'views/schedulers.xml',
            ],
    'installable': True,
}
