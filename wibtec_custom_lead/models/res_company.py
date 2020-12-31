import json
import logging
from datetime import datetime
import requests
from dateutil.parser import parse as duparse
from odoo import api, fields, models
from odoo.exceptions import Warning

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = "res.company"

    def open_sync_wz(self):
        view_ref = self.env['ir.model.data'].get_object_reference('wibtec_custom_lead', 'sync_lead_wizard_form')
        view_id = view_ref and view_ref[1] or False,
        if view_id:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Sync Lead',
                'res_model': 'sync.lead.wizard',
                'view_mode': 'form',
                'view_id': view_id,
                'target': 'new',
                'nodestroy': True,
            }

