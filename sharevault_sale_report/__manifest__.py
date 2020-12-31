#! -*- encoding: utf-8 -*-
{
    'name': "ShareVault Sale Report",
    'version': '13.0.1.0.20',
    'author' : 'Wibtec',
    'website': 'http://www.wibtec.com',
    'category': 'Extra tools',
    'summary': 'Sales',
    'description': 'Sales',
    'depends': [
                'sharevault',
                'sale'
                ],
    'data': [
                'views/report_sale_order.xml',
                'views/sale_views.xml',
                ],
    'installable': True,
}
