# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    postpone_email_sunday = fields.Boolean('Sunday')
    postpone_email_monday = fields.Boolean('Monday')
    postpone_email_tuesday = fields.Boolean('Tuesday')
    postpone_email_wednesday = fields.Boolean('Wednesday')
    postpone_email_thursday = fields.Boolean('Thursday')
    postpone_email_friday = fields.Boolean('Friday')
    postpone_email_saturday = fields.Boolean('Saturday')
