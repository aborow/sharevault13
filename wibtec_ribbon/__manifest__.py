#! -*- encoding: utf-8 -*-
{
    'name': "Wibtec Ribbon",
    'version': '13.0.1.0.0',
    'category': 'Web',
    'author': 'Wibtec',
    'website': 'http://www.wibtec.com',
    'license': 'AGPL-3',
    "depends": [
        'web', 'web_enterprise'
        ],
    "data": [
        'data/ribbon_data.xml',
        'view/base_view.xml',
        ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
    "auto_install": False,
    'installable': True
}
