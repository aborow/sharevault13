# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from lxml import etree


class ResPartner(models.Model):
    _inherit = "res.partner"

    inv_dash = fields.Boolean(string="Invoices", default=True)
    so_dash = fields.Boolean(string="Sales", default=True)
    lead_dash = fields.Boolean(string="Leads", default=True)

    def get_result(self):
        for item in self:
            if item.inv_dash and item.so_dash == False and item.lead_dash == False:
                return {
                    'name': _('See dashboard'),
                    'view_mode': 'form',
                    'res_model': 'board.board',
                    'binding_model': 'res.partner',
                    'view_id': self.env.ref('wibtec_contact_overview.board_partner_form_i').id,
                    'type': 'ir.actions.act_window',
                    'context': {
                        'default_partner_id': item.id,
                    },
                }
            if item.inv_dash == False and item.so_dash == False and item.lead_dash:
                return {
                    'name': _('See dashboard'),
                    'view_mode': 'form',
                    'res_model': 'board.board',
                    'binding_model': 'res.partner',
                    'view_id': self.env.ref('wibtec_contact_overview.board_partner_form_l').id,
                    'type': 'ir.actions.act_window',
                    'context': {
                        'default_partner_id': item.id,
                    },
                }
            if item.inv_dash == False and item.so_dash and item.lead_dash == False:
                return {
                    'name': _('See dashboard'),
                    'view_mode': 'form',
                    'res_model': 'board.board',
                    'binding_model': 'res.partner',
                    'view_id': self.env.ref('wibtec_contact_overview.board_partner_form_s').id,
                    'type': 'ir.actions.act_window',
                    'context': {
                        'default_partner_id': item.id,
                    },
                }

            if item.inv_dash and item.so_dash and item.lead_dash == False:
                return {
                    'name': _('See dashboard'),
                    'view_mode': 'form',
                    'res_model': 'board.board',
                    'binding_model': 'res.partner',
                    'view_id': self.env.ref('wibtec_contact_overview.board_partner_form_is').id,
                    'type': 'ir.actions.act_window',
                    'context': {
                        'default_partner_id': item.id,
                    },
                }
            if item.inv_dash == False and item.so_dash and item.lead_dash:
                return {
                    'name': _('See dashboard'),
                    'view_mode': 'form',
                    'res_model': 'board.board',
                    'binding_model': 'res.partner',
                    'view_id': self.env.ref('wibtec_contact_overview.board_partner_form_ls').id,
                    'type': 'ir.actions.act_window',
                    'context': {
                        'default_partner_id': item.id,
                    },
                }
            if item.inv_dash and item.so_dash == False and item.lead_dash:
                return {
                    'name': _('See dashboard'),
                    'view_mode': 'form',
                    'res_model': 'board.board',
                    'binding_model': 'res.partner',
                    'view_id': self.env.ref('wibtec_contact_overview.board_partner_form_il').id,
                    'type': 'ir.actions.act_window',
                    'context': {
                        'default_partner_id': item.id,
                    },
                }
            if item.inv_dash and item.so_dash and item.lead_dash:
                return {
                    'name': _('See dashboard'),
                    'view_mode': 'form',
                    'res_model': 'board.board',
                    'binding_model': 'res.partner',
                    'view_id': self.env.ref('wibtec_contact_overview.board_partner_form').id,
                    'type': 'ir.actions.act_window',
                    'context': {
                        'default_partner_id': item.id,
                    } ,
                }
            if item.inv_dash == False and item.so_dash == False and item.lead_dash == False:
                return {
                    'name': _('See dashboard'),
                    'view_mode': 'form',
                    'res_model': 'board.board',
                    'binding_model': 'res.partner',
                    'view_id': self.env.ref('wibtec_contact_overview.board_partner_form_f').id,
                    'type': 'ir.actions.act_window',
                    'context': {
                        'default_partner_id': item.id,
                    },
                }


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
        domain = self._context.get('default_partner_id')
        str_d = "[['partner_id', '='," + str(domain) + "]]"
        for node in doc.iter(tag="action"):
            if node.attrib.get("id", '') == 'action_lead':
                node.attrib.update({'domain': str_d})
            if node.attrib.get("id", '') == 'action_invoice':
                node.attrib.update({'domain': str_d})
            if node.attrib.get("id", '') == 'action_sales':
                node.attrib.update({'domain': str_d})
        res['arch'] = etree.tostring(doc)
        return res