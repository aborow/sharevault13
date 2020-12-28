# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Event(models.Model):
    _inherit = 'event.event'

    @api.depends('name')
    def name_get(self):
        result = []
        for event in self:
            result.append((event.id, '%s' % (event.name)))
        return result
