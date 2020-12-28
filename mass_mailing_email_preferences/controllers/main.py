# -*- coding: utf-8 -*-
from odoo import fields, http, tools, _, exceptions
from odoo.http import request
from odoo.tools import consteq


class UnsubscribeList(http.Controller):

    SV_FIELDS = [
                'email_preference_marketing',
                'email_preference_white_papers',
                'email_preference_events',
                'email_preference_blog',
                'email_preference_company_news',
                'email_preference_product_news'
                ]

    def _valid_unsubscribe_tokens(self, email, token):
        if not (email):
            return False
        result = consteq(request.env['res.partner'].generate_token(email), token)
        return result

    @http.route('/update/contact', type='http', auth='public', website=True)
    def update_value_in_contact(self, email=None, token="", **kw):
        if email:
            partner = request.env['res.partner'].sudo().search([('email','=',email)])
            if not self._valid_unsubscribe_tokens(email, str(token)):
                raise exceptions.AccessDenied()
            vals = {}
            if partner:
                for k in self.SV_FIELDS:
                    vals[k] = eval('partner.' + k)

                try:
                    opt_out = partner.opt_out
                    if opt_out:
                        vals['opt_out'] = opt_out
                except:
                    vals['opt_out'] = False
                    pass

                if email:
                    vals['email'] = email
                if partner:
                    vals['is_partner'] = True
                return request.render('mass_mailing_email_preferences.unsubscribe_mass_mailing',vals)

    @http.route('/updated/contact', type='http', auth='public', website=True)
    def updated_contact(self, **kw):
        if request.httprequest.method == 'POST':
            partner_vals = {}
            for k in self.SV_FIELDS:
                partner_vals[k] = True if kw.get(k) == 'on' else False

            partner = request.env['res.partner'].sudo()\
                                .search([('email', '=', kw.get('email'))])
            if partner:
                partner_vals['opt_out'] = True if kw.get('opt_out', False) == 'on' else False
                partner.write(partner_vals)

            return http.request.render('mass_mailing_email_preferences.unsubscribe_page', {})
