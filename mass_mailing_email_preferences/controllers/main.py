# -*- coding: utf-8 -*-
from odoo import fields, http, tools, _, exceptions
from odoo.http import request
from odoo.addons.mass_mailing.controllers.main import MassMailController


class UnsubscribeList(http.Controller):

    @http.route('/update/contact', type='http', auth='public', website=True)
    def update_value_in_contact(self, **kw):
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
            partner = request.env['res.partner'].search([('email', '=', email)])
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


class MassMailInheritController(MassMailController):

    @http.route(['/mail/mailing/<int:mailing_id>/unsubscribe'], type='http', website=True, auth='public')
    def mailing(self, mailing_id, email=None, res_id=None, token="", **post):
        mailing = request.env['mailing.mailing'].sudo().browse(mailing_id)
        if mailing.exists():
            res_id = res_id and int(res_id)
            if not self._valid_unsubscribe_token(mailing_id, res_id, email, str(token)):
                raise exceptions.AccessDenied()

            if mailing.mailing_model_real == 'mailing.contact':
                # Unsubscribe directly + Let the user choose his subscriptions
                mailing.update_opt_out(email, mailing.contact_list_ids.ids, True)

                contacts = request.env['mailing.contact'].sudo().search(
                    [('email_normalized', '=', tools.email_normalize(email))])
                subscription_list_ids = contacts.mapped('subscription_list_ids')
                # In many user are found : if user is opt_out on the list with contact_id 1 but not with contact_id 2,
                # assume that the user is not opt_out on both
                # TODO DBE Fixme : Optimise the following to get real opt_out and opt_in
                opt_out_list_ids = subscription_list_ids.filtered(lambda rel: rel.opt_out).mapped('list_id')
                opt_in_list_ids = subscription_list_ids.filtered(lambda rel: not rel.opt_out).mapped('list_id')
                opt_out_list_ids = set([list.id for list in opt_out_list_ids if list not in opt_in_list_ids])

                unique_list_ids = set([list.list_id.id for list in subscription_list_ids])
                list_ids = request.env['mailing.list'].sudo().browse(unique_list_ids)
                unsubscribed_list = ', '.join(str(list.name) for list in mailing.contact_list_ids if list.is_public)
                return request.render('mass_mailing.page_unsubscribe', {
                    'contacts': contacts,
                    'list_ids': list_ids,
                    'opt_out_list_ids': opt_out_list_ids,
                    'unsubscribed_list': unsubscribed_list,
                    'email': email,
                    'mailing_id': mailing_id,
                    'res_id': res_id,
                    'show_blacklist_button': request.env['ir.config_parameter'].sudo().get_param(
                        'mass_mailing.show_blacklist_buttons'),
                })
            else:
                opt_in_lists = request.env['mailing.contact.subscription'].sudo().search([
                    ('contact_id.email_normalized', '=', email),
                    ('opt_out', '=', False)
                ]).mapped('list_id')
                blacklist_rec = request.env['mail.blacklist'].sudo()._add(email)
                self._log_blacklist_action(
                    blacklist_rec, mailing_id,
                    _("""Requested blacklisting via unsubscribe link."""))
                partner = request.env['res.partner'].search([('email', '=', email)])
                is_partner = False
                if partner:
                    is_partner = True
                return request.render('mass_mailing.page_unsubscribed', {
                    'email': email,
                    'mailing_id': mailing_id,
                    'res_id': res_id,
                    'list_ids': opt_in_lists,
                    'show_blacklist_button': request.env['ir.config_parameter'].sudo().get_param(
                        'mass_mailing.show_blacklist_buttons'),
                    'is_partner': is_partner,
                })
        return request.redirect('/web')
