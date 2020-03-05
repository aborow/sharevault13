# -*- coding: utf-8 -*-
from odoo import api, fields, models


class MassMailing(models.Model):
    _inherit = "mailing.mailing"

    state = fields.Selection(
        [('draft', 'Draft'), ('in_queue', 'In Queue'), ('sending', 'Sending'), ('done', 'Sent'), ('error', 'Error')],
        string='Status', required=True, tracking=True, copy=False, default='draft', group_expand='_group_expand_states')

    @api.model
    def _process_mass_mailing_queue(self):
        mass_mailings = self.search(
            [('state', 'in', ('in_queue', 'sending')), '|', ('schedule_date', '<', fields.Datetime.now()),
             ('schedule_date', '=', False)])
        for mass_mailing in mass_mailings:
            try:
                user = mass_mailing.write_uid or self.env.user
                mass_mailing = mass_mailing.with_context(**user.with_user(user).context_get())
                if len(mass_mailing._get_remaining_recipients()) > 0:
                    mass_mailing.state = 'sending'
                    mass_mailing.action_send_mail()
                else:
                    mass_mailing.write({'state': 'done', 'sent_date': fields.Datetime.now()})
            except Exception:
                mass_mailings.state = 'error'