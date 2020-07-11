# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # return the data models that connect to res.partner as oe2many
    @api.model
    def _get_action_domain(self):
        allowed_models = ['res.partner']
        model_id = self.env.ref('base.model_res_partner').id
        fields = self.env['ir.model.fields'].search([
                                                    ('model_id','=',model_id),
                                                    ('ttype','=','one2many'),
                                                    ])
        for f in fields:
            if f.relation not in allowed_models:
                allowed_models.append(f.relation)
        domain = [
                    ('type','=','ir.actions.act_window'),
                    ('context','not ilike','active_id')
                    ]
        if allowed_models:
            domain.append(('res_model','in',allowed_models))
        return domain


    partner_dashboard_action_ids = fields.Many2many(
                                        comodel_name='ir.actions.act_window',
                                        relation='settings_dashboard_rel',
                                        domain=_get_action_domain
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
        try:
            action_ids = params.get_param('wibtec_partner_dashboard.partner_dashboard_action_ids', False)
            action_ids = action_ids[action_ids.find("(")+1:action_ids.find(")")].replace(' ','')
            if action_ids.endswith(","):
                action_ids = action_ids[:-1]
            action_ids = list(action_ids.split(","))
            try:
                for i in range(0, len(action_ids)):
                    action_ids[i] = int(action_ids[i])
            except Exception as e:
                _logger.error(e)
                pass
            if action_ids:
                res.update(partner_dashboard_action_ids=[(6,0,action_ids)])
        except Exception as e2:
            _logger.error(e2)
            pass
        return res


    @api.constrains('partner_dashboard_action_ids')
    def rebuild_partner_dashboard(self):
        view_id = self.env.ref('wibtec_partner_dashboard.board_partner_form')
        aux = '<action name="%s" string="%s" view_mode="list" context="{}" domain="[]" modifiers="{}" id="%s"/>'
        actions = []
        for a in self.partner_dashboard_action_ids:
            actions.append("<board style='1'>\n<column>")
            actions.append(aux % (a.id, a.name, a.id))
            actions.append("</column>\n<column/>\n<column/>\n</board>\n")
        start = "<?xml version='1.0'?>\n<form string='Dashboard'>\n"
        end = "</form>"
        if actions:
            aux_arch = ''.join(actions)
        else:
            aux_arch = ''
        view_id.write({'arch_base':start + aux_arch + end})
