#! -*- encoding: utf-8 -*-
{
    'name': "Website Custom Pages",
    'version': '13.0.1.0.31',
    'author': 'Wibtec',
    'website': 'http://www.wibtec.com',
    'category': 'Website',
    'summary': 'Changes to website mode',
    'description': """
- SV-120
- SV-130
- adds live chat
    """,
    'depends': [
                'web',
                'website_form',
                'website_crm',
                'web_editor',
                'documents',
                'utm',
                'website_blog',
                'base_automation',
                'website_links',
                'sharevault_suppression_list',
                'website_event_questions',
                'website_event_questions_free_text'
                ],
    'data': [
            'security/ir.model.access.csv',
            'data/mail_template_data.xml',
            'data/utm_source_data.xml',
            'data/base_automation_data.xml',
            'wizard/website_create_page.xml',
            'views/snippets.xml',
            'views/web_thankyou_pages_view.xml',
            'views/lead_views.xml',
            'views/event_view.xml',
            'views/blog_view.xml',
            'views/document_view.xml',
            'views/source.xml',
            'views/website_blog.xml',
            'views/website_page.xml',
            ],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
}
