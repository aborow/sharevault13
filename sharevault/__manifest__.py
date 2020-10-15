# -*- coding: utf-8 -*-
{
    'name': 'ShareVault',
    'version': '13.0.1.0.30',
    'category': 'Tools',
    'author': 'Wibtec',
    'website': 'www.wibtec.com',
    'summary': 'Setup for ShareVault',
    'description': """

Version(1.1) - ShareVault data model
Version(1.2) - Added constraint on the email field for partner.
13.0.1.0.1 - New Fields in Contact object - "Opt Out" and "Source ID".
13.0.1.0.2 - New Commit add it just for Adding changes in the odoo.sh.
13.0.1.0.3 - change to define Xpath for new added field because Error displayed in the odoo.sh.
13.0.1.0.6 - [SV-53] hided fields based on company type.
13.0.1.0.11 - [SV-46] Industry / Sub Industry / Accounting Industry.
13.0.1.0.13 - [SV-66] add new fields to Sharevault Module.
""",
    'depends': [
                'crm',
                #'auditlog',
                'helpdesk',
                'sale_management',
                'account',
                #'sic_code'
                'base',
                'sale',
                'account',
                'website_partner',
                'account_reports',
                'sms',
                'mail',
                ],
    'data': [
            'security/groups_data.xml',
            'security/ir.model.access.csv',
            'data/ir_cron.xml',
            #'data/auditlog_data.xml',
            #'data/generic_data.xml',
            'views/sharevault_view.xml',

            'views/partner_view.xml',
            'views/crm_view.xml',

            'views/templates.xml',
            ],
    'installable': True,
    'auto_install': False,
}
