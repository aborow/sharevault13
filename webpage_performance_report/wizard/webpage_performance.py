# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from datetime import datetime


class WebpagePerformance(models.TransientModel):
    _name = "webpage.performance"
    _description = "Webpage Performance Report"

    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')
    page_ids = fields.Many2many('website.page', string='Pages')

    def get_page_name(self):
        pages = self.env['website.page'].search([('id', 'in', self.page_ids.ids)])
        return pages

    def get_view(self, id):
        track = self.env['website.track'].search([('page_id', '=', id)])
        start_date = datetime.combine(self.from_date, datetime.min.time())
        end_date = datetime.combine(self.to_date, datetime.min.time())
        track_filter = track.filtered(lambda p: start_date <= p.visit_datetime <= end_date)
        count = 0
        if track:
            count = len([i.id for i in track_filter])
        return count

    def get_first_visit(self, id):
        track = self.env['website.track'].search([('page_id', '=', id)])
        start_date = datetime.combine(self.from_date, datetime.min.time())
        end_date = datetime.combine(self.to_date, datetime.min.time())
        track_filter = track.filtered(lambda p: start_date <= p.visit_datetime <= end_date)
        date = ''
        if track_filter:
            date = self.env['website.track'].browse(sorted(track_filter)[0].id)
            first_visit = datetime.strptime(str(date.visit_datetime.date()), '%Y-%m-%d')
            return first_visit.strftime("%m/%d/%Y")
        return ''

    def get_submission(self, id):
        track = self.env['website.track'].search([('page_id', '=', id)])
        start_date = datetime.combine(self.from_date, datetime.min.time())
        end_date = datetime.combine(self.to_date, datetime.min.time())
        track_filter = track.filtered(lambda p: start_date <= p.visit_datetime <= end_date)
        if track_filter:
            submission_rate = track_filter.mapped('visitor_id').filtered(lambda r: r.lead_count != 0)
            sr = sum(sr.lead_count for sr in submission_rate)
            return sr
        return 0

    @api.model
    def default_get(self, fields):
        res = super(WebpagePerformance, self).default_get(fields)
        res_ids = self._context.get('active_ids')
        res.update({
            'page_ids': res_ids,
        })
        return res

    def print_pdf(self):
        return self.env.ref('webpage_performance_report.report_page_performance_report').report_action(self)
