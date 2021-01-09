#! -*- encoding: utf-8 -*-
{
    'name': "Mass mailing - save domain",
    'version': '13.0.1.0.11',
    'author' : 'Wibtec',
    'website': 'http://www.wibtec.com',
    'category': 'Extra tools',
    'summary': 'Save domains for mass mailing',
    'description': """
- Save domains for mass mailing
- Create favourite searches for contacts out of the saved lists
""",
    'depends': [
                'web',
                'mass_mailing',
                'contacts',
                'base_automation'
                ],
    'data': [
                'security/ir.model.access.csv',
                'data/base_automation_data.xml',
                'wizard/mail_view.xml',
                'views/mail_view.xml'
                ],
    'installable': True,
}
