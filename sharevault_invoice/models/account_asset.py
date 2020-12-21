# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
_logger = logging.getLogger(__name__)


class AccountAsset(models.Model):
    _inherit = 'account.asset'

    has_neg_value = fields.Boolean('Has Negative Value')

    @api.depends('original_move_line_ids', 'original_move_line_ids.account_id', 'asset_type')
    def _compute_value(self):
        res = super(AccountAsset, self)._compute_value()
        for record in self:
            total_credit = sum(line.credit for line in record.original_move_line_ids)
            total_debit = 0.00
            for line in record.original_move_line_ids:
                if line.account_id and (line.account_id.can_create_asset) and line.account_id.create_asset != 'no':
                        total_debit -= line.debit
            if record.model_id and total_debit < 0 :
                record.has_neg_value = True
        return res

    @api.onchange('model_id')
    def _onchange_model_id(self):
        res = super(AccountAsset, self)._onchange_model_id()
        model = self.model_id
        if model:
            if self.has_neg_value:
                self.account_depreciation_id = model.account_depreciation_expense_id
                self.account_depreciation_expense_id = model.account_depreciation_id
            else:
                self.account_depreciation_id = model.account_depreciation_id
                self.account_depreciation_expense_id = model.account_depreciation_expense_id
