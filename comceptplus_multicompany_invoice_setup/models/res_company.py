# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class Company(models.Model):
    _inherit = 'res.company'

    """
    @api.onchange('default_invoice_template')
    def onchange_default_invoice_template(self):
        #set the external_report_layout
        pass
    """

    default_invoice_template_with_payments = fields.Many2one('ir.ui.view',
                                                string='Default invoice template (with payments)',
                                                domain=[('type','=','qweb')],
                                                help='Select what kind of body of the invoice document (with payments) is to be used',
                                                readonly=False
                                                )
    default_invoice_template_without_payments = fields.Many2one('ir.ui.view',
                                                string='Default invoice template (without payments)',
                                                domain=[('type','=','qweb')],
                                                help='Select what kind of body of the invoice document (without payments) is to be used',
                                                readonly=False
                                                )
