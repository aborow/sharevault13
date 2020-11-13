# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime
import requests
from dateutil.parser import parse as duparse
from odoo import api, fields, models
from odoo.exceptions import Warning

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = "res.company"

    @api.model
    def _default_update_datetime(self):
        date = str(datetime.strptime("1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"))
        return datetime.strptime("1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")

    # Company level QuickBooks Configuration fields
    sf_client_id = fields.Char(help="The client ID you obtain from the developer dashboard.", string="Consumer Key")
    sf_client_secret = fields.Char(help="The client secret you obtain from the developer dashboard.", string="Consumer Secret")

    sf_auth_base_url = fields.Char('Authorization URL', default="https://login.salesforce.com/services/oauth2/authorize",
                                   help="User authenticate uri")
    sf_access_token_url = fields.Char('Authorization Token URL', default="https://login.salesforce.com/services/oauth2/token",
                                      help="Exchange code for refresh and access tokens")
    sf_request_token_url = fields.Char('Redirect URL', default="http://localhost:8069/get_auth_code",
                                       help="One of the redirect URIs listed for this project in the developer dashboard.")
    sf_url = fields.Char(default="https://", help="SalesForce API URIs, use access token to call SalesForce API's", string="Instance URL")

    # used for api calling, generated during authorization process.
    sf_auth_code = fields.Char('Auth Code', help="")
    sf_access_token = fields.Char('Access Token', help="The token that must be used to access the SALESFORCE API.")
    sf_refresh_token = fields.Char('Refresh Token')

    account_lastmodifieddate = fields.Datetime("Account Last Modified Time", default=_default_update_datetime)
    contact_lastmodifieddate = fields.Datetime("Contact Last Modified Time", default=_default_update_datetime)


    def sanitize_data(self, field_to_sanitize):
        '''
            This method sanitizes the data to remove UPPERCASE and 
            spaces between field chars
            @params : field_to_sanitize(char)
            @returns : field_to_sanitize(char)
        '''
        return field_to_sanitize.strip()

    def get_headers(self, type=False):
        headers = {}
        headers['Authorization'] = 'Bearer ' + str(self.sf_access_token)
        headers['accept'] = 'application/json'
        if type:
            headers['Content-Type'] = 'application/json'
        else:
            headers['Content-Type'] = 'text/plain'
        return headers

    def test(self):
        if self.sf_access_token:
            headers = {}
            headers['Authorization'] = 'Bearer ' + str(self.sf_access_token)
            headers['accept'] = 'application/json'
            headers['Content-Type'] = 'text/plain'
            data = requests.request('GET', self.sf_url + '/services/data/v39.0/sobjects/connectedapplication', headers=headers)
            if data.status_code == 200:
                return self.sendMessage("CONNECTION SUCCESSFUL")
            if data.status_code == 401:
                self.refresh_token_from_access_token()
                return self.sendMessage("Session expired or invalid")
            else:
                raise Warning("CONNECTION UNSUCCESSFUL")

    def refresh_token_from_access_token(self):
        '''
            This method gets access token from refresh token
            and grant type is refresh_token, 
            This token will be long lived.
        '''
        if not self.sf_refresh_token:
            raise Warning("Please authenticate first.")
        refresh_token_data = {}
        headers = {
            'content-type': "application/x-www-form-urlencoded"
        }
        sf_refresh_token = self.sanitize_data(self.sf_refresh_token)
        sf_client_id = self.sanitize_data(self.sf_client_id)
        sf_client_secret = self.sanitize_data(self.sf_client_secret)
        sf_url = self.sanitize_data(self.sf_url)

        refresh_token_data.update({
            'grant_type': 'refresh_token',
            'refresh_token': sf_refresh_token,
            'client_id': sf_client_id,
            'client_secret': sf_client_secret
        })
        refresh_token_response = requests.post(sf_url + '/services/oauth2/token',
                                               data=refresh_token_data,
                                               headers=headers)
        if refresh_token_response.status_code == 200:
            try:
                # try getting JSON repr of it
                parsed_response = refresh_token_response.json()
                if 'access_token' in parsed_response:
                    _logger.info("REFRESHING ACCESS TOKEN {}".format(parsed_response.get('access_token')))
                    self.sf_access_token = parsed_response.get('access_token')
            except Exception as ex:
                raise Warning("EXCEPTION : {}".format(ex))
        elif refresh_token_response.status_code == 401:
            _logger.error("Access token/refresh token is expired")
        else:
            raise Warning("We got a issue !!!! Desc : {}".format(refresh_token_response.text))




    @api.model
    def _scheduler_login_aunthetication(self):
        company_id = self.env['res.users'].search([('id', '=', self.env.user.id)], limit=1).company_id
        if self.env.user.company_id:
            self.env.user.company_id.refresh_token_from_access_token()

    def login(self):

        url = self.sf_auth_base_url + '?client_id=' + self.sf_client_id + '&redirect_uri=' + self.sf_request_token_url + '&response_type=code&display=popup'
        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "new"
        }

    def sendMessage(self, message):
        view_ref = self.env['ir.model.data'].get_object_reference('odoo_salesforce_connector', 'salseforce_message_wizard_form')
        view_id = view_ref and view_ref[1] or False,
        if view_id:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Message',
                'res_model': 'salseforce.message.wizard',
                'view_mode': 'form',
                'view_id': view_id,
                'context': {'message': message},
                'target': 'new',
                'nodestroy': True,
            }

