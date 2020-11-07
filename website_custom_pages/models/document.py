# -*- coding: utf-8 -*-
from odoo import api, fields, models

class DocumentShare(models.Model):
    _inherit = 'documents.share'

    tracked_link_id = fields.Many2one('link.tracker', 'Tracked link')
