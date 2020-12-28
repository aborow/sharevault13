# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ReportSvMailingHashIntegrity(models.AbstractModel):
    _name = 'report.sv_mailing.report_mailing_template'
    _description = 'Mailing Template'

    def get_link_report(self):
        for rec in self:
            lt_object = self.env['link.tracker'].search([('mass_mailing_id', '=', rec.id)])

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['mailing.mailing'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'mailing.mailing',
            'docs': docs,
        }
