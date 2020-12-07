# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
_logger = logging.getLogger(__name__)


class AccountAsset(models.Model):
    _inherit = 'account.asset'

    @api.depends('original_move_line_ids', 'original_move_line_ids.account_id', 'asset_type')
    def _compute_value(self):
        res = super(AccountAsset, self)._compute_value()
        for record in self:
            total_credit = sum(line.credit for line in record.original_move_line_ids)
            total_debit = 0.00
            for line in record.original_move_line_ids:
                if line.account_id and (line.account_id.can_create_asset) and line.account_id.create_asset != 'no':
                        total_debit -= line.debit
            record.original_value = total_credit + total_debit
        return res