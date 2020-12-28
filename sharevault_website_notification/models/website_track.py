# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import ValidationError
import json
import logging
from datetime import datetime
import requests
_logger = logging.getLogger(__name__)
from datetime import datetime
import datetime

class WebsiteTrack(models.Model):
    _inherit = "website.track"

    @api.model
    def send_notify_mail(self):
        for rec in self:
            if rec.page_id.notify:
                if rec.visitor_id:
                    if rec.visitor_id.lead_ids:
                        lead = rec.visitor_id.lead_ids.ids[0]
                        lead_rec = self.env['crm.lead'].search([('id','=',lead)])
                        if lead_rec:
                            if lead_rec.user_id.email and rec.visitor_id.email:
                                if lead_rec.user_id.email == rec.visitor_id.email:
                                    wvti_obj = self.env['website.visitor.track.info'].search([('visitor_id','=',rec.visitor_id.id)])
                                    if wvti_obj:
                                        wvti_obj.write({'visitor_info_ids': [(0, 0, {
                                            'page_id': rec.page_id.id,
                                            'track_id': rec.id,
                                        })]})
                                    else:
                                        wvti_obj = self.env['website.visitor.track.info']
                                        wvti_obj.create({'visitor_id': rec.visitor_id.id})
                                        wvti_obj.write({'visitor_info_ids': [(0, 0, {
                                            'page_id': rec.page_id.id,
                                            'track_id': rec.id,
                                        })]})

            if not rec.page_id.notify:
                if rec.page_id:
                    date_with_time = datetime.datetime.today() - datetime.timedelta(days=1)
                    if rec.visitor_id.email and rec.visitor_id.latest_revisit:
                        if not rec.visitor_id.website_track_ids or rec.visitor_id.create_date >= datetime.datetime.today() - datetime.timedelta(days=1) or rec.visitor_id.latest_revisit >= date_with_time.date() or rec.visitor_id.email.split('@')[1] == 'sharevault.com':
                            wvti_obj = self.env['website.visitor.track.info'].search(
                                [('visitor_id', '=', rec.visitor_id.id)])
                            if wvti_obj:
                                wvti_obj.write({'visitor_info_ids': [(0, 0, {
                                    'page_id': rec.page_id.id,
                                    'track_id': rec.id,
                                })]})
                            else:
                                wvti_obj = self.env['website.visitor.track.info']
                                wvti_obj.create({'visitor_id': rec.visitor_id.id})
                                wvti_obj.write({'visitor_info_ids': [(0, 0, {
                                    'page_id': rec.page_id.id,
                                    'track_id': rec.id,
                                })]})


class WebsitePage(models.Model):
    _inherit = "website.page"

    notify = fields.Boolean('Notify', default=False)


class WebsiteVisitor(models.Model):
    _inherit = "website.visitor"

    latest_revisit = fields.Date('Latest Revisit Date', default=lambda self: fields.Date.today())


class WebsiteVisitorTrackInfo(models.Model):
    _name = "website.visitor.track.info"
    _description = "Website Visitor Track Info"

    visitor_id = fields.Many2one('website.visitor', string="Visitor")
    visitor_info_ids = fields.One2many('website.visitor.track.info.line', 'track_info_id', string="Website Track Info")


    @api.model
    def send_track_mail(self):
        for rec in self.search([]):
            if rec.visitor_info_ids:
                template = self.env['mail.template'].search(
                    [('name', '=', 'ShareVault: Website Track Notification from Scheduler')], limit=1)
                if template:
                    if rec.visitor_id.email:
                        server = rec.env['ir.mail_server'].search([], order='sequence asc', limit=1)
                        values = template.generate_email(rec.id, fields=None)
                        values['mail_server_id'] = server.id
                        values['email_from'] = rec.env.user.email
                        values['email_to'] = rec.visitor_id.email
                        values['recipient_ids'] = False
                        values['message_type'] = "email"
                        values['res_id'] = False
                        values['reply_to'] = False
                        values['author_id'] = self.env['res.users'].browse(
                            rec.env.uid).partner_id.id
                        mail_mail_obj = self.env['mail.mail']
                        msg_id = mail_mail_obj.sudo().create(values)
                        if msg_id:
                            msg_id.send()
                            rec.visitor_id.latest_revisit = fields.Date.today()
                            rec.visitor_info_ids = False

        return True


class WebsiteVisitorTrackInfoLine(models.Model):
    _name = "website.visitor.track.info.line"
    _description = "Website Visitor Track Info Line"

    track_info_id = fields.Many2one('website.visitor.track.info', string="Visitor Info")
    page_id = fields.Many2one('website.page', string="Page")
    track_id = fields.Many2one('website.track', string="Track")