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

    # Initially, we needed to save this in order to send a confirmation email afterwards
    # but, after changes required by SV, we now keep it, in order to have a relation
    # between the lead and the shared link used
    typ_id = fields.Many2one('web.thankyou.pages','Thank You Message')

    share_link_id = fields.Many2one('documents.share', 'Shared Link')

    #tracked_link_id = fields.Many2one('link.tracker', 'Tracked link')
