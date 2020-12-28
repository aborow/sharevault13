# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleOrderLines(models.Model):
    _inherit = "sale.order.line"

    months = fields.Selection([('12', '12'),
                                   ('6', '6'),
                                   ('1', '1'),
                                   ], string="Months")

class SaleOrder(models.Model):
    _inherit = "sale.order"

    payment_method = fields.Many2one('account.payment.method','Payment Method')
    subscription_terms = fields.Selection([('12', '12 Months'),
                                   ('6', '6 Months'),
                                   ('1', '1 Month'),
                                   ], string="Subscription Term")
    expiration_date = fields.Date('Expiration')
    payment_frequency = fields.Selection([('1', 'One Time'),
                                           ], string="Payment Frequency")
    total_discount = fields.Float('Total Discount')
    monthly_total = fields.Float('Monthly Total')
    due_upone_receipt = fields.Float('Due Upon Receipt')
    # authorized_contact_name = fields.Many2one("res.partner",'Authorized Contact Name')
    # authorized_contact_title = fields.Char('Authorized Contact Title')
    authorized_contact_signature = fields.Char('Authorized Contact Signature')





