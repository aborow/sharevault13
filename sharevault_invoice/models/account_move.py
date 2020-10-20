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


    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        res = super(AccountMove, self)._onchange_partner_id()
        if self.partner_id.company_type == 'company':
            return {'domain': {'sharevault_id': [('partner_id', '=', self.partner_id.id)]}}
        if self.partner_id.company_type == 'person':
            return {'domain': {'sharevault_id': [('sharevault_owner', '=', self.partner_id.id)]}}
        return res

    sharevault_id = fields.Many2one('sharevault.sharevault', 'ShareVault',
                                        readonly=True,
                                        states={'draft': [('readonly', False)]})
    sales_type = fields.Selection([('new', 'New Customer'),
                                   ('cs', 'Customer Success'),
                                   ('renewal', 'Renewal')], string="Sales Type")
    date_creation = fields.Date('Creation')
    date_expiration = fields.Date('Expiration')
    customer_contact_id = fields.Many2one('res.partner',string="Customer Contact")
    amount_paid = fields.Monetary('Amount Paid',compute='get_amount_paid')

    @api.depends('amount_residual','amount_total')
    def get_amount_paid(self):
        for move in self:
            if move.amount_residual:
                move.amount_paid = move.amount_total - move.amount_residual
            if move.invoice_payment_state == 'paid':
                if move.amount_residual == 0.0:
                    move.amount_paid = move.amount_total

class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'


    # @api.constrains('analytic_account_id')
    # def _constraint_analytic_account_id(self):
    #     if self.move_id.type == 'in_invoice' and not self.analytic_account_id:
    #         raise ValidationError(_("WARNING: No Analytic Account Found"))