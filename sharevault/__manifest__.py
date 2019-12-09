# -*- coding: utf-8 -*-
{
    'name': 'ShareVault',
    'version': '1.2',
    'category': 'Tools',
    'author': 'Wibtec',
    'website': 'www.wibtec.com',
    'summary': 'Setup for ShareVault',
    'description': """

Version(1.1) - ShareVault data model
Version(1.2) - Added constraint on the email field for partner.
""",
    'depends': [
                'crm',
                #'auditlog',
                'helpdesk',
                'sale_management',
                'account',
                #'sic_code'
                ],
    'data': [
            'security/groups_data.xml',
            'security/ir.model.access.csv',
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
