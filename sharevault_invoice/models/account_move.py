# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):

    _inherit = 'account.move'

    # load the dates when selecting a sharevault
    # related fields are not being used to make sure the values don't get
    # changed once the invoice is issued
    @api.onchange('sharevault_id')
    def onchange_sharevault_id(self):
        self.ensure_one()
        self.date_creation = self.sharevault_id \
                                and self.sharevault_id.date_creation or False
        self.date_expiration = self.sharevault_id \
                                and self.sharevault_id.date_expiration or False


    sharevault_id = fields.Many2one('sharevault.sharevault', 'ShareVault',
                                        readonly=True,
                                        states={'draft': [('readonly', False)]}
                                        )
    date_creation = fields.Date('Creation')
    date_expiration = fields.Date('Expiration')
    customer_contact_id = fields.Many2one('res.partner',string="Customer Contact")