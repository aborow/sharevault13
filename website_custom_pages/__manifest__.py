#! -*- encoding: utf-8 -*-
{
    'name': "Website Custom Pages",
    'version': '13.0.1.0.1',
    'author': 'Wibtec',
    'website': 'http://www.wibtec.com',
    'category': 'Website',
    'summary': 'Custom pages snippets as per hubspot',
    'description': """SV-120: Landing page migration POC
    """,
    'depends': ['website', 'crm', 'website_form'],
    'data': [
            'security/ir.model.access.csv',
            'views/snippets.xml',
            'views/web_thankyou_pages_view.xml',
            ],
    'installable': True,
}
