# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):

    _inherit = 'account.move'

    # load the dates when selecting a sharevault
    # related fields are not being used to make sure the values don't get
    # changed once the invoice is issued
    @api.onchange('partner_id', 'sharevault_id')
    def onchange_sharevault_id(self):
        self.ensure_one()
        self.date_creation = self.sharevault_id \
                                and self.sharevault_id.sv_creation_dt or False
        self.date_expiration = self.sharevault_id \
                                and self.sharevault_id.sv_expiration_dt or False
        if self.sharevault_id:
            self.customer_contact_id = self.sharevault_id and self.sharevault_id.sharevault_owner.id or False
            self.term_end_date = self.sharevault_id \
                                 and self.sharevault_id.sv_expiration_dt or False
            self.quota_pages = self.sharevault_id \
                                 and self.sharevault_id.quota_pages or False
        else:
            self.term_start_date = False
            self.term_end_date = False
            self.customer_contact_id = False


    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        res = super(AccountMove, self)._onchange_partner_id()
        self.sharevault_id = False
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
                                   ('renewal', 'Renewal'),
                                   ('mtm', 'Month-to-Month')], string="Sales Type")
    date_creation = fields.Date('Creation')
    date_expiration = fields.Date('Expiration')
    customer_contact_id = fields.Many2one('res.partner',string="Customer Contact")
    amount_paid = fields.Monetary('Amount Paid',compute='get_amount_paid')
    term_start_date = fields.Date('Term Start Date',
                                  readonly=True,
                                  states={'draft': [('readonly', False)]})
    term_end_date = fields.Date('Term End Date',
                                readonly=True,
                                states={'draft': [('readonly', False)]})
    quota_mb = fields.Char('Quota: MB (Size in GB)', compute='get_quota_mb')
    quota_pages = fields.Char('Quota: pages')

    def get_cancel_invoices(self):
        invoices_list = []
        move_lines = []
        payment_list = []
        move_line = self.env['account.move.line'].search([('parent_state','=','cancel')])
        for ml in move_line:
            move_lines.append(str(ml.id))
        payment = self.env['account.payment'].search([('state','=','cancelled')])
        for pay in payment:
            payment_list.append(str(pay.id))
        invoices = self.search([('state', '=', 'cancel')])
        for inv in invoices:
            invoices_list.append(str(inv.id))
        if move_lines:
            self.env.cr.execute(""" DELETE FROM  account_move_line WHERE id in %s""", (tuple(move_lines),))
        if payment_list:
            self.env.cr.execute(""" DELETE FROM  account_payment WHERE id in %s""", (tuple(payment_list),))
        if invoices_list:
            self.env.cr.execute(""" DELETE FROM  account_move WHERE id in %s""", (tuple(invoices_list),))


    @api.depends('sharevault_id','partner_id')
    def get_quota_mb(self):
        for move in self:
            if move.sharevault_id:
                if move.sharevault_id.quota_mb >= 1000:
                    move.quota_mb = int(move.sharevault_id.quota_mb/1000)
                else:
                    move.quota_mb = move.sharevault_id.quota_mb/1000
            else:
                move.quota_mb = ''
    # message_follower_ids = fields.One2many(
    #     'mail.followers', 'res_id', string='Followers', copy=True)

    @api.depends('amount_residual','amount_total')
    def get_amount_paid(self):
        for move in self:
            if move.amount_residual:
                move.amount_paid = move.amount_total - move.amount_residual
            else:
                if move.amount_residual == 0.0:
                    move.amount_paid = move.amount_total
            if move.invoice_payment_state == 'paid':
                if move.amount_residual == 0.0:
                    move.amount_paid = move.amount_total

    def _auto_create_asset(self):
        create_list = []
        invoice_list = []
        auto_validate = []
        for move in self:
            if not move.is_invoice():
                continue

            for move_line in move.line_ids.filtered(lambda line: not (move.type in ('out_invoice', 'out_refund') and line.account_id.user_type_id.internal_group == 'asset')):
                if (
                    move_line.account_id
                    and (move_line.account_id.can_create_asset)
                    and move_line.account_id.create_asset != "no"
                    and not move.reversed_entry_id
                    and not (move_line.currency_id or move.currency_id).is_zero(move_line.price_total)
                    and not move_line.asset_id
                ):
                    if not move_line.name:
                        raise UserError(_('Journal Items of {account} should have a label in order to generate an asset').format(account=move_line.account_id.display_name))
                    vals = {
                        'name': move_line.product_id.display_name,
                        'company_id': move_line.company_id.id,
                        'currency_id': move_line.company_currency_id.id,
                        'account_analytic_id': move_line.analytic_account_id.id,
                        'analytic_tag_ids': [(6, False, move_line.analytic_tag_ids.ids)],
                        'original_move_line_ids': [(6, False, move_line.ids)],
                        'state': 'draft',
                    }
                    model_id = move_line.account_id.asset_model
                    if model_id:
                        vals.update({
                            'model_id': model_id.id,
                        })
                    auto_validate.append(move_line.account_id.create_asset == 'validate')
                    invoice_list.append(move)
                    create_list.append(vals)

        assets = self.env['account.asset'].create(create_list)
        for asset, vals, invoice, validate in zip(assets, create_list, invoice_list, auto_validate):
            if 'model_id' in vals:
                asset._onchange_model_id()
                asset._onchange_method_period()
                if validate:
                    asset.validate()
            if invoice:
                asset_name = {
                    'purchase': _('Asset'),
                    'sale': _('Deferred revenue'),
                    'expense': _('Deferred expense'),
                }[asset.asset_type]
                msg = _('%s created from invoice') % (asset_name)
                msg += ': <a href=# data-oe-model=account.move data-oe-id=%d>%s</a>' % (invoice.id, invoice.name)
                asset.message_post(body=msg)
        return assets


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    is_expense = fields.Boolean('Is Expensed', default=False, compute='_get_expense_account')

    @api.depends('account_id','move_id.partner_id','product_id')
    def _get_expense_account(self):
        for line in self:
            if line.move_id.type == 'in_invoice':
                if line.account_id.user_type_id.name == 'Expenses':
                    line.is_expense = True
                else:
                    line.is_expense = False
            else:
                line.is_expense = False
                if self._context.get('default_type') == 'entry':
                    if line.account_id.user_type_id.name == 'Expenses':
                        line.is_expense = True
                    else:
                        line.is_expense = False
    # @api.constrains('analytic_account_id')
    # def _constraint_analytic_account_id(self):
    #     if self.move_id.type == 'in_invoice' and not self.analytic_account_id:
    #         raise ValidationError(_("WARNING: No Analytic Account Found"))