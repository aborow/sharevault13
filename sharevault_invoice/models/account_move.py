# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
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
                                and self.sharevault_id.sv_creation_dt or False
        self.date_expiration = self.sharevault_id \
                                and self.sharevault_id.sv_expiration_dt or False


    sharevault_id = fields.Many2one('sharevault.sharevault', 'ShareVault',
                                        readonly=True,
                                        states={'draft': [('readonly', False)]}
                                        )
    date_creation = fields.Date('Creation')
    date_expiration = fields.Date('Expiration')
    customer_contact_id = fields.Many2one('res.partner',string="Customer Contact")
    amount_paid = fields.Monetary('Amount Paid',compute='get_amount_paid')

    @api.depends('amount_residual','amount_total')
    def get_amount_paid(self):
        for move in self:
            if self.amount_residual:
                self.amount_paid = self.amount_total - self.amount_residual

class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'


    # @api.constrains('analytic_account_id')
    # def _constraint_analytic_account_id(self):
    #     if self.move_id.type == 'in_invoice' and not self.analytic_account_id:
    #         raise ValidationError(_("WARNING: No Analytic Account Found"))