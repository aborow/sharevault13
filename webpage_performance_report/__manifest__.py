#! -*- encoding: utf-8 -*-
{
    'name': "Page Performance Report",
    'version': '13.0.1.0.0',
    'author': 'Wibtec',
    'website': 'http://www.wibtec.com',
    'category': 'Website',
    'summary': 'SV-243: Page performance Reports (Summary and Individual)',
    'description': 'Print Performance report based on the selected pages and period',
    'depends': [
        'website', 'web'
    ],
    'data': [
        'wizard/webpage_performance_views.xml',
        'report/page_performance_templates.xml',
        'views/website_page_views.xml',
    ],
    'installable': True,
}
