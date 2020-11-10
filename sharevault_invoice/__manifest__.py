#! -*- encoding: utf-8 -*-
{
    'name': "ShareVault invoice",
    'version': '13.0.1.0.20',
    'author' : 'Wibtec',
    'website': 'http://www.wibtec.com',
    'category': 'Extra tools',
    'summary': 'Invoice',
    'description': 'Invoice',
    'depends': [
                'sharevault',
                'account',
                'l10n_us_check_printing',
                'sale'
                ],
    'data': [
                'data/paper_format.xml',
                'views/account_invoice.xml',
                'views/external_layout.xml',
                'views/report_invoice.xml',
                'views/product_template_view.xml',
                'views/print_check_top.xml',
                'views/report_check_top_view.xml',
                'views/sale_view.xml'
                ],
    'installable': True,
}
