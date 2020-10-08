#! -*- encoding: utf-8 -*-
{
    'name': "Website Custom Pages",
    'version': '13.0.1.0.19',
    'author': 'Wibtec',
    'website': 'http://www.wibtec.com',
    'category': 'Website',
    'summary': 'Custom pages snippets as per hubspot',
    'description': """SV-120: Landing page migration POC
    """,
    'depends': [
                'website',
                'crm',
                'website_form',
                'website_crm',
                'web_editor',
                'documents',
                'utm',
                'website_blog'
                ],
    'data': [
            'security/ir.model.access.csv',
            'views/snippets.xml',
            'views/web_thankyou_pages_view.xml',
            'views/lead_views.xml',
            'views/blog_view.xml',
            'views/website_blog.xml',
            ],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
}
