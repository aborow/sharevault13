# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class HistQbInfo(models.Model):
    _name = "hist.qb.info"
    _description = "Historical Info"

    hist_qb_acc_type = fields.Char('Hist QB Account Type')
    hist_pqb_name = fields.Char('Hist Partner QB Name')
    hist_item = fields.Char('Hist Item')
    hist_qty = fields.Float('Hist Qty')
    hist_sales_price = fields.Float('Hist Sales Price')
    move_id = fields.Many2one('account.move', string='Move')


class AccountMove(models.Model):
    _inherit = "account.move"

    hist_type = fields.Char('Hist Type')
    hist_num = fields.Char('Hist Number')
    hist_sv_name = fields.Char('Hist Sharevault Name')
    hist_rep = fields.Char('Hist Representative')
    hist_pay_method = fields.Char('Hist Pay Method')
    hist_qba_type_ids = fields.One2many('hist.qb.info', 'move_id', string='Hist Info')