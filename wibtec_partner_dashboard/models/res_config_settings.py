# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    partner_dashboard_action_ids = fields.Many2many(
                                        comodel_name='ir.actions.act_window',
                                        relation='settings_dashboard_rel',
                                        check_company=True,
                                        domain=[
                                                ('type','=','ir.actions.act_window'),
                                                ('view_mode','ilike','tree')
                                                ]
                                        )

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        params = self.env['ir.config_parameter'].sudo()
        params.set_param("wibtec_partner_dashboard.partner_dashboard_action_ids",
                                             self.partner_dashboard_action_ids)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        action_ids = params.get_param('wibtec_partner_dashboard.partner_dashboard_action_ids', False)
        action_ids = action_ids[action_ids.find("(")+1:action_ids.find(")")].replace(' ','')
        if action_ids.endswith(","):
            action_ids = action_ids[:-1]
        action_ids = list(action_ids.split(","))
        for i in range(0, len(action_ids)):
            action_ids[i] = int(action_ids[i])
        if action_ids:
            res.update(partner_dashboard_action_ids=[(6,0,action_ids)])
        return res

    @api.constrains('partner_dashboard_action_ids')
    def rebuild_partner_dashboard(self):
        view_id = self.env.ref('wibtec_partner_dashboard.board_partner_form')
        aux = '<action name="%s" string="%s" view_mode="list" context="%s" domain="[]" modifiers="{}" id="ãction_%s"/>'
        actions = []
        for a in self.partner_dashboard_action_ids:
            actions.append("<board style='1'>\n<column>")
            actions.append(
                            aux % (
                                a.id,
                                a.name,
                                a.context.replace('\n','').replace('  ',''),
                                a.id
                                )
                            )
            actions.append("</column>\n<column/>\n<column/>\n</board>\n")
        if actions:
            _logger.info(actions)
            aux_arch = "<?xml version='1.0'?>\n<form string='Dashboard'>\n" \
                        + ''.join(actions) \
                        + "</form>"
            view_id.write({'arch_base':aux_arch})

        _logger.info(aux_arch)
        _logger.info("BBBBBBBBBBBBBBBBBBBBBB")
