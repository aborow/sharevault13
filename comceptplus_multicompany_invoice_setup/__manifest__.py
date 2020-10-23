#! -*- encoding: utf-8 -*-
{
    'name': "comceptPLUS: multicompany invoice setup",
    'version': '1.0',
    'author' : 'comceptPLUS',
    'website': 'https://comceptplus.com',
    'category': 'Tools',
    'description': """

This module was supposed to lay out the foundation for dynamic invoice template
loading, according to what would be defined in the company record. Unfortunately,
due to dynamic qweb t-call not being possible since v10, a different approach
was made.

This module creates the same structure as it would for the original purpose but
the chosen template will only be used as boolean. It will be up to every module
implementing a new invoice to inherit and change Odoo's report loading.

Here, the only thing done is to change report loading in order to use default
templates only if no company-specific template has been set.

Two fields become available, in the company form, for the user to define which
layouts to load for invoices (with/without payments).
""",
    'depends': [
                'account',
                'comceptplus_multicompany_reports'
                ],
    'data': [
            'views/res_company_view.xml',
            'views/template.xml'
            ],
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
