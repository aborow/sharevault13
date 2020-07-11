# -*- coding: utf-8 -*-
#import logging
from lxml import etree
from odoo import api, fields, models, _
#_logger = logging.getLogger(__name__)


class Board(models.AbstractModel):
    _inherit = "board.board"

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        """
        Overrides orm field_view_get.
        @return: Dictionary of Fields, arch and toolbar.
        """
        res = super(Board, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        doc = etree.XML(res['arch'])
        """
        The domain and the context defined in the action would not work in the dashboard, so
        we add the domain right here
        """
        for node in doc.iter(tag="action"):
            # Get the domain defined in the action and pass it to the action,
            # added with the partner_id
            aux_id = int(node.attrib['id'].replace(',',''))
            action = self.env['ir.actions.act_window'].sudo().browse(aux_id)
            domain = action.domain
            domain_partner = str(('partner_id','=',self._context.get('default_partner_id')))
            if domain:
                domain = domain.replace('[', '[' + domain_partner + ',')
            else:
                domain = "[" + domain_partner + "]"
            node.attrib.update({'domain': domain})
        res['arch'] = etree.tostring(doc)
        return res
