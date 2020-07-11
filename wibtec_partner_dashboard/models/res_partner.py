# -*- coding: utf-8 -*-
import logging
import re
from odoo import api, fields, models, _
_logger = logging.getLogger(__name__)

class Partner(models.Model):
    _inherit = "res.partner"

    def get_partner_dashboard(self):
        for item in self:
            """
            Because we stick to the original actions and their context will not
            be overriden by the context in the dashboard view, we need to use
            domain
            """
            view = self.env.ref('wibtec_partner_dashboard.board_partner_form')
            #domain = 'domain="' + str([('partner_id','=',item.id)]) + '"'
            #regex = 'domain="\[.*?\]"'
            #aux = re.sub(regex, domain, view.arch_base)
            #view.write({'arch_base': aux})

            # PROBLEM!!! - when the view is loaded, the changes are not assumed
            # and it is necessary to reload the page

            #self.env['ir.ui.view'].flush(["arch_base"])

            # Make sure the record is updated by the time the view is called
            #self._cr.execute("""
            #                UPDATE ir_ui_view
            #                SET arch_db = '%s'
            #                WHERE id=%s
            #                """ % (
            #                        aux.replace("'","''"),
            #                        view.id
            #                        )
            #                )
            #self.env.cr.commit()

            return {
                    'type': 'ir.actions.act_window',
                    'name': _('Dashboard'),
                    'view_mode': 'form',
                    'res_model': 'board.board',
                    'binding_model': 'res.partner',
                    'view_id': view.id,
                    }
