# Copyright 2015 Francesco OpenCode Apruzzese <cescoap@gmail.com>
# Copyright 2016 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# Copyright 2017 Thomas Binsfeld <thomas.binsfeld@acsone.eu>
# Copyright 2017 Xavier Jiménez <xavier.jimenez@qubiq.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Web Environment Ribbon",
    'version': '12.0.1.0.1',
    'category': 'Web',
    'author': 'Francesco OpenCode Apruzzese, '
              'Tecnativa, '
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/web',
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
