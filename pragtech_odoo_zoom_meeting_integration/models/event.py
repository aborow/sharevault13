# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
import requests
from odoo.exceptions import UserError


class EventEvent(models.Model):
    """Event"""
    _inherit = 'event.event'

    meet_flag = fields.Boolean('Create Zoom Event', default=False)
    password = fields.Char(string='Meet Password')
    create_flag = fields.Boolean('Flag', default=False)
    meet_url = fields.Text(string='Meet URL')
    meet_id = fields.Text(string='Meet ID')
    meet_pwd = fields.Text(string='Meet Password')
    zoom_event_type = fields.Selection([('meeting', 'Zoom Meeting'),
                                        ('webinar', 'Zoom Webinar')], string="Zoom Event Type")

    @api.model
    def create(self, vals):
        res = super(EventEvent, self).create(vals)
        if vals.get('meet_flag'):
            res.post_request_meet1()
        return res

    def post_request_meet1(self):
        company_id = self.env['res.users'].search([('id', '=', self._context.get('uid'))]).company_id
        if self.env.user.company_id:
            self.env.user.company_id.refresh_token_from_access_token()

        if company_id.zoom_access_token and company_id.zoom_refresh_token:
            zoom_access_token = company_id.sanitize_data(company_id.zoom_access_token)

            bearer = 'Bearer ' + zoom_access_token
            payload = {}
            headers = {
                'Content-Type': "application/json",
                'Authorization': bearer
            }

            st_time = self.date_begin
            start_time = str(st_time).replace(' ', 'T') + 'Z'

            ed_time = self.date_end
            end_time = str(ed_time).replace(' ', 'T') + 'Z'
            diff = ed_time - st_time
            minutes = diff.total_seconds() / 60
            if self.zoom_event_type == "meeting":
                data = {
                    "topic": self.name,
                    "type": "2",
                    "start_time": start_time,
                    "duration": str(round(minutes)),
                    "timezone": "NA",
                    "password": self.password,
                    "agenda": self.name,
                    "recurrence": {
                        "type": "2",
                        "repeat_interval": "3",
                        "end_times": "5",
                        "end_date_time": end_time
                    },
                    "settings": {
                        "approval_type": 0,
                        "host_video": True,
                        "participant_video": True,
                        "registrants_email_notification": True

                    }
                }
                meet_response = requests.request("POST", "https://api.zoom.us/v2/users/me/meetings", headers=headers,
                                                 json=data)

                if meet_response.status_code == 200 or meet_response.status_code == 201:
                    data_rec = meet_response.json()
                    self.write({"meet_url": data_rec.get('join_url'), "meet_id": data_rec.get('id'),
                                "meet_pwd": data_rec.get('password'), "create_flag": True})

                elif meet_response.status_code == 401:
                    raise UserError("Please Authenticate with Zoom Meet.")
            if self.zoom_event_type == "webinar":
                data = {
                    "topic": self.name,
                    "type": 5,
                    "start_time": start_time,
                    "duration": str(round(minutes)),
                    "timezone": "NA",
                    "password": self.password,
                    "agenda": self.name,
                    "recurrence": {
                        "type": 1,
                        "repeat_interval": 1,
                        "end_date_time": end_time
                    },
                    "settings": {
                        "host_video": "true",
                        "panelists_video": "true",
                        "practice_session": "true",
                        "hd_video": "true",
                        "approval_type": 0,
                        "registration_type": 2,
                        "audio": "both",
                        "auto_recording": "none",
                        "enforce_login": "false",
                        "close_registration": "true",
                        "show_share_button": "true",
                        "allow_multiple_devices": "false",
                        "registrants_email_notification": "true"
                    }
                }
                meet_response = requests.request("POST", "https://api.zoom.us/v2/users/me/webinars", headers=headers,
                                                 json=data)
                if meet_response.status_code == 200 or meet_response.status_code == 201:
                    data_rec = meet_response.json()
                    self.write({"meet_url": data_rec.get('join_url'), "meet_id": data_rec.get('id'),
                                "meet_pwd": data_rec.get('password'), "create_flag": True})

                elif meet_response.status_code == 401:
                    raise UserError("Please Authenticate with Zoom Webinar.")


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    def post_request_meet_recipients(self):
        company_id = self.env['res.users'].search([('id', '=', self._context.get('uid'))]).company_id
        if self.env.user.company_id:
            self.env.user.company_id.refresh_token_from_access_token()

        if company_id.zoom_access_token and company_id.zoom_refresh_token:
            zoom_access_token = company_id.sanitize_data(company_id.zoom_access_token)

            bearer = 'Bearer ' + zoom_access_token
            headers = {
                'Content-Type': "application/json",
                'Authorization': bearer
            }

            data = {
                "email": self.email,
                "first_name": self.name,
            }
            if self.event_id.zoom_event_type == "meeting":
                url = "https://api.zoom.us/v2/meetings/%s/registrants" % self.event_id.meet_id
            if self.event_id.zoom_event_type == "webinar":
                url = "https://api.zoom.us/v2/webinars/%s/registrants" % self.event_id.meet_id
            meet_response = requests.request("POST", url, headers=headers,
                                             json=data)
            if meet_response.status_code == 200 or meet_response.status_code == 201:
                data_rec = meet_response.json()
                self.write({"meet_url": data_rec.get('join_url'), "meet_id": data_rec.get('id'),
                            "meet_pwd": self.event_id.meet_pwd,
                            "registrant_id": data_rec.get('registrant_id'),
                            'start_time': data_rec.get('start_time'),
                            'topic': data_rec.get('topic')})

            elif meet_response.status_code == 401:
                raise UserError("Please Authenticate with Zoom Meet.")

    @api.model
    def create(self, vals):
        registration = super(EventRegistration, self).create(vals)
        if registration.event_id.meet_flag:
            registration.post_request_meet_recipients()
        return registration

    meet_url = fields.Text(string='Meet URL')
    meet_id = fields.Text(string='Meet ID')
    meet_pwd = fields.Text(string='Meet Password')
    registrant_id = fields.Text(string='Participant ID')
    start_time = fields.Text(string="Start Time")
    topic = fields.Text(string="Topic")
