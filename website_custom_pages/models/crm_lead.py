# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Lead(models.Model):
    _inherit = 'crm.lead'

    information_sharing = fields.Selection([('1_m', '1 Month'),
                                            ('3_m', '3 Months'),
                                            ('6_m', '6 Months'),
                                            ('1_y', '1 Year'),
                                            ('share_third',
                                             'We are currently sharing confidential documents with third parties.'),
                                            ('use_sharevault',
                                             'We currently use ShareVault.'),
                                            ('dont_sharevault',
                                             'We dont use ShareVault, but we are currently sharing confidential documentation with third parties.'),
                                            ], 'Information Sharing', store=True)
    share_link_id = fields.Many2one('documents.share', 'Shared Link')
    tracked_link_id = fields.Many2one('link.tracker', 'Tracked link')

    # We need to save this in order to send a confirmation email afterwards
    typ_id = fields.Many2one('web.thankyou.pages','Thank You Message')
