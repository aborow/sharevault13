# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    postpone_email_sunday = fields.Boolean('Sunday')
    postpone_email_monday = fields.Boolean('Monday')
    postpone_email_tuesday = fields.Boolean('Tuesday')
    postpone_email_wednesday = fields.Boolean('Wednesday')
    postpone_email_thursday = fields.Boolean('Thursday')
    postpone_email_friday = fields.Boolean('Friday')
    postpone_email_saturday = fields.Boolean('Saturday')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        Config = self.env['ir.config_parameter'].sudo()
        for d in self.DAYS:
            res['postpone_email_' + d] = Config.get_param('postpone_email_' + d, default=False)
        return res

    @api.model
    def set_values(self):
        Config = self.env['ir.config_parameter'].sudo()
        for d in self.DAYS:
            Config.sudo().set_param('postpone_email_' + d, eval('self.postpone_email_' + d))
        super(ResConfigSettings, self).set_values()
