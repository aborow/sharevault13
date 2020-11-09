# -*- coding: utf-8 -*-
from itertools import groupby
import matplotlib.pyplot as plt
import io
import base64
from odoo import fields, models, api


class MassMailing(models.Model):
    _inherit = "mailing.mailing"

    def get_link_report(self):
        for rec in self:
            lt_object = self.env['link.tracker'].search([('mass_mailing_id', '=', rec.id)])
            return lt_object

    def get_contacts(self):
        for rec in self:
            mailing_trace = self.env['mailing.trace'].search([('mass_mailing_id', '=', rec.id)])
            val = mailing_trace.filtered(lambda p: p.model == 'res.partner' and p.opened != False)
            mt_group = groupby(val, lambda r: r.res_id)
            result = []
            for partner_id, records in mt_group:
                partner_obj = self.env['res.partner'].browse(partner_id)
                if partner_obj:
                    result.append({'partner_id': partner_obj.name if partner_obj.name else False,
                                   'opened': len(list(trace.id for trace in records if records))})
            return result

    def get_contacts_c(self):
        for rec in self:
            mailing_trace = self.env['mailing.trace'].search([('mass_mailing_id', '=', rec.id)])
            val = mailing_trace.filtered(lambda p: p.model == 'res.partner' and p.clicked)
            mt_group = groupby(val, lambda r: r.res_id)
            result = []
            for partner_id, records in mt_group:
                partner_obj = self.env['res.partner'].browse(partner_id)
                if partner_obj:
                    clicked = len(list(trace.id for trace in records))
                    result.append({'partner_id': partner_obj.name, 'clicked': clicked})
            return result

    def get_unsubscribers(self):
        for rec in self:
            mcs = self.env['mailing.contact.subscription'].search_count(
                [('list_id', 'in', rec.contact_list_ids.ids), ('unsubscription_date', '!=', False)])
            return mcs

    def get_chart_image(self):
        x_open_list = []
        y_open_list = []
        x_click_list = []
        y_click_list = []
        image_64 = ''
        for rec in self:
            mailing_trace = self.env['mailing.trace'].search([('mass_mailing_id', '=', rec.id)])
            val_clicked = mailing_trace.filtered(lambda p: p.model == 'res.partner' and p.clicked)
            val_opened = mailing_trace.filtered(lambda p: p.model == 'res.partner' and p.opened)
            for o in val_opened:
                x_open_list.append(o.opened)
                y_open_list.append(1)
            for c in val_clicked:
                x_click_list.append(c.clicked)
                y_click_list.append(1)
        fig, ax = plt.subplots(figsize=(6, 4))
        if x_open_list or x_click_list:
            plt.plot(x_open_list, y_open_list, 'o-')
            plt.plot(x_click_list, y_click_list, 'o-')
            plt.title('')
            plt.xlabel('')
            plt.ylim(bottom=0)
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            image_64 = base64.b64encode(buf.read())
        return image_64
