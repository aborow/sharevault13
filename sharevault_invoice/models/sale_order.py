# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        super(SaleOrder, self).onchange_partner_id()
        self.sharevault_id = False
        if self.partner_id.company_type == 'company':
            return {'domain': {'sharevault_id': [('partner_id', '=', self.partner_id.id)]}}
        if self.partner_id.company_type == 'person':
            return {'domain': {'sharevault_id': [('sharevault_owner', '=', self.partner_id.id)]}}


    sharevault_id = fields.Many2one('sharevault.sharevault', 'ShareVault',
                                        readonly=True,
                                        states={'draft': [('readonly', False)]})
    sales_type = fields.Selection([('new', 'New Customer'),
                                   ('cs', 'Customer Success'),
                                   ('renewal', 'Renewal')], string="Sales Type")
    term_start_date = fields.Date('Term Start Date',
                                  readonly=True,
                                  states={'draft': [('readonly', False)]})
    term_end_date = fields.Date('Term End Date',
                                readonly=True,
                                states={'draft': [('readonly', False)]})
    customer_contact_id = fields.Many2one('res.partner', string="Customer Contact")


    @api.onchange('partner_id', 'sharevault_id')
    def onchange_sharevault_id(self):
        if self.sharevault_id:
            self.customer_contact_id = self.sharevault_id and self.sharevault_id.sharevault_owner.id or False
            self.term_start_date = self.sharevault_id.term_start_date
            self.term_end_date = self.sharevault_id.term_end_date
        else:
            self.customer_contact_id = False
            self.term_start_date = False
            self.term_end_date = False

    def _prepare_invoice(self):
        result = super(SaleOrder, self)._prepare_invoice()
        if self.sales_type:
            result.update({'sales_type': self.sales_type})
        if self.sharevault_id:
            result.update({'sharevault_id': self.sharevault_id.id})
        if self.term_start_date:
            result.update({'term_start_date': self.term_start_date})
        if self.term_end_date:
            result.update({'term_end_date': self.term_end_date})
        if self.customer_contact_id:
            result.update({'customer_contact_id': self.customer_contact_id.id})
        return result
