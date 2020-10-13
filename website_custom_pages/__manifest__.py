#! -*- encoding: utf-8 -*-
{
    'name': "Website Custom Pages",
    'version': '13.0.1.0.20',
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
                'website_blog',
                'base_automation',
                'website_links'
                ],
    'data': [
            'security/ir.model.access.csv',
            'data/mail_template_data.xml',
            'data/utm_source_data.xml',
            'data/base_automation_data.xml',
            'views/snippets.xml',
            'views/web_thankyou_pages_view.xml',
            'views/lead_views.xml',
            'views/blog_view.xml',
            'views/website_blog.xml',
            'views/website_page.xml',
            ],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
}
