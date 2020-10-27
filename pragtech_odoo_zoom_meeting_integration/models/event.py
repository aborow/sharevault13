# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
import requests
from odoo.exceptions import UserError


class EventEvent(models.Model):
    """Event"""
    _inherit = 'event.event'

    meet_flag = fields.Boolean('Add Zoom Meet', default=False)
    password = fields.Char(string='Meet Password')
    create_flag = fields.Boolean('Flag', default=False)
    meet_url = fields.Text(string='Meet URL')
    meet_id = fields.Text(string='Meet ID')
    meet_pwd = fields.Text(string='Meet Password')

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

            data = {
                "topic": self.name,
                "type": "2",
                "start_time": start_time,
                "duration": "5",
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
