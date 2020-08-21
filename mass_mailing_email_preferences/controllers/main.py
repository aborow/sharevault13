# -*- coding: utf-8 -*-
from odoo import fields, http, tools, _, exceptions
from odoo.http import request
from odoo.tools import consteq


class UnsubscribeList(http.Controller):

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
                confirmation_email = partner.email_preference_confirmation
                if confirmation_email:
                    vals['confirmation_email'] = confirmation_email
                customer_updates = partner.email_preference_customer_updates
                if customer_updates:
                    vals['customer_updates'] = customer_updates
                hubspot_blog = partner.email_preference_hubspot_blog
                if hubspot_blog:
                    vals['hubspot_blog'] = hubspot_blog
                life_science = partner.email_preference_life_science
                if life_science:
                    vals['life_science'] = life_science
                mergers_webinars = partner.email_preference_merger
                if mergers_webinars:
                    vals['mergers_webinars'] = mergers_webinars
                marketing_information = partner.email_preference_marketing
                if marketing_information:
                    vals['marketing_information'] = marketing_information
                sv_blog_subscription = partner.email_preference_sv_blog
                if sv_blog_subscription:
                    vals['sv_blog_subscription'] = sv_blog_subscription
                sv_comp_info = partner.email_preference_sv_company_info
                if sv_comp_info:
                    vals['sv_comp_info'] = sv_comp_info
                sv_product_info = partner.email_preference_sv_product_info
                if sv_product_info:
                    vals['sv_product_info'] = sv_product_info
                sv_subscription = partner.email_preference_sv_subscription
                if sv_subscription:
                    vals['sv_subscription'] = sv_subscription
                one_to_one = partner.email_preference_one
                if one_to_one:
                    vals['one_to_one'] = one_to_one
                sc_message = partner.email_preference_subscription_confirmation
                if sc_message:
                    vals['sc_message'] = sc_message
                if email:
                    vals['email'] = email
                if partner:
                    vals['is_partner'] = True
                return request.render('mass_mailing_email_preferences.unsubscribe_mass_mailing',vals)

    @http.route('/updated/contact', type='http', auth='public', website=True)
    def updated_contact(self, **kw):
        if request.httprequest.method == 'POST':
            confirmation_email = kw.get('confirmation_email')
            customer_updates = kw.get('customer_updates')
            hubspot_blog = kw.get('hubspot_blog')
            life_science = kw.get('life_science')
            mergers_webinars = kw.get('mergers_webinars')
            marketing_information = kw.get('marketing_information')
            sv_blog_subscription = kw.get('sv_blog_subscription')
            sv_comp_info = kw.get('sv_comp_info')
            sv_product_info = kw.get('sv_product_info')
            sv_subscription = kw.get('sv_subscription')
            one_to_one = kw.get('one_to_one')
            sc_message = kw.get('sc_message')
            email = kw.get('email')
            partner = request.env['res.partner'].sudo().search([('email', '=', email)])
            if partner:
                partner.write({'email_preference_confirmation': True if confirmation_email == 'on' else False,
                               'email_preference_customer_updates': True if customer_updates == 'on' else False,
                               'email_preference_hubspot_blog': True if hubspot_blog == 'on' else False,
                               'email_preference_life_science': True if life_science == 'on' else False,
                               'email_preference_merger': True if mergers_webinars == 'on' else False,
                               'email_preference_marketing': True if marketing_information == 'on' else False,
                               'email_preference_sv_blog': True if sv_blog_subscription == 'on' else False,
                               'email_preference_sv_company_info': True if sv_comp_info == 'on' else False,
                               'email_preference_sv_product_info': True if sv_product_info == 'on' else False,
                               'email_preference_sv_subscription': True if sv_subscription == 'on' else False,
                               'email_preference_one': True if one_to_one == 'on' else False,
                               'email_preference_subscription_confirmation': True if sc_message == 'on' else False,
                               })

            return http.request.render('mass_mailing_email_preferences.unsubscribe_page', {})
