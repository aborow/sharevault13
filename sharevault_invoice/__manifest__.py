#! -*- encoding: utf-8 -*-
{
    'name': "ShareVault invoice",
    'version': '13.0.1.0.2',
    'author' : 'Wibtec',
    'website': 'http://www.wibtec.com',
    'category': 'Extra tools',
    'summary': 'Invoice',
    'description': 'Invoice',
    'depends': [
                'sharevault',
                ],
    'data': [
                'data/paper_format.xml',
                'views/account_invoice.xml',
                'views/external_layout.xml',
                'views/report_invoice.xml'
                ],
    'installable': True,
}
