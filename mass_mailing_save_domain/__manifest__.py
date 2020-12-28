#! -*- encoding: utf-8 -*-
{
    'name': "Mass mailing - save domain",
    'version': '13.0.1.0.10',
    'author' : 'Wibtec',
    'website': 'http://www.wibtec.com',
    'category': 'Extra tools',
    'summary': 'Save domains for mass mailing',
    'description': 'Save domains for mass mailing',
    'depends': [
                'web',
                'mass_mailing'
                ],
    'data': [
                'security/ir.model.access.csv',
                'wizard/mail_view.xml',
                'views/mail_view.xml'
                ],
    'installable': True,
}
