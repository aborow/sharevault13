# -*- coding: utf-8 -*-
from odoo import api, fields, models, _,tools
import hashlib
import hmac
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    def generate_url(self, email=""):
        context = dict(self._context or {})
        add_val_ids = context.get('active_ids')
        partner_obj = self.env['res.partner']
        for val_id in add_val_ids:
            partner_brw = partner_obj.browse(val_id)
            if partner_brw.email:
                email = partner_brw.email
            else:
                raise ValidationError(_('Enter a email for generate URL'))
            secret = self.env["ir.config_parameter"].sudo().get_param("database.secret")
            url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
            token = (self.env.cr.dbname, tools.ustr(email))
            result = hmac.new(secret.encode('utf-8'), repr(token).encode('utf-8'), hashlib.sha512).hexdigest()
            email = email.replace('@', '%40')
            finalurl = url + '/update/contact?email=' + email + '&token=' + result
            partner_brw.write({'generated_url': finalurl})

    #email_preference_confirmation = fields.Boolean('Confirmation Email', default=True)
    email_preference_customer_updates = fields.Boolean('Customer Updates', default=True)
    email_preference_hubspot_blog = fields.Boolean('Default HubSpot Blog Subscription', default=True)
    email_preference_life_science = fields.Boolean('Life Sciences White Papers, Webinars and Useful News', default=True)
    email_preference_merger = fields.Boolean('Mergers & Acquisitions White Papers, Webinars, and Useful News', default=True)
    email_preference_marketing = fields.Boolean('Marketing Information', default=True)
    email_preference_sv_blog = fields.Boolean('ShareVault Blog Subscription', default=True)
    email_preference_sv_company_info = fields.Boolean('ShareVault Company Information', default=True)
    email_preference_sv_product_info = fields.Boolean('ShareVault Product Information', default=True)
    email_preference_sv_subscription = fields.Boolean('ShareVault Subscription', default=True)
    email_preference_one = fields.Boolean('One to One', default=True)
    email_preference_subscription_confirmation = fields.Boolean('Subscriptions Confirmation Message', default=True)
    generated_url = fields.Text('Email Webpage URL')

    def generate_token(self, email=False):
        secret = self.env["ir.config_parameter"].sudo().get_param("database.secret")
        token = (self.env.cr.dbname, tools.ustr(email))
        result = hmac.new(secret.encode('utf-8'), repr(token).encode('utf-8'), hashlib.sha512).hexdigest()
        return result


    @api.onchange(
                    #'email_preference_confirmation',
                    'email_preference_customer_updates',
                    'email_preference_hubspot_blog','email_preference_life_science',
                    'email_preference_merger','email_preference_marketing',
                    'email_preference_sv_blog','email_preference_sv_company_info',
                    'email_preference_sv_product_info','email_preference_sv_subscription',
                    'email_preference_one','email_preference_subscription_confirmation')
    def onchange_email_preferences(self):
        if any([
                #self.email_preference_confirmation,
                self.email_preference_customer_updates,
                self.email_preference_hubspot_blog,
                self.email_preference_life_science,
                self.email_preference_merger,
                self.email_preference_marketing,
                self.email_preference_sv_blog,
                self.email_preference_sv_company_info,
                self.email_preference_sv_product_info,
                self.email_preference_sv_subscription,
                self.email_preference_one,
                self.email_preference_subscription_confirmation
                ]
            ):
            self.opt_out = False


    @api.onchange('opt_out')
    def onchange_opt_out(self):
        if self.opt_out:
            vals = {
                    #'email_preference_confirmation':False,
                    'email_preference_customer_updates':False,
                    'email_preference_hubspot_blog':False,
                    'email_preference_life_science':False,
                    'email_preference_merger':False,
                    'email_preference_marketing':False,
                    'email_preference_sv_blog':False,
                    'email_preference_sv_company_info':False,
                    'email_preference_sv_product_info':False,
                    'email_preference_sv_subscription':False,
                    'email_preference_one':False,
                    'email_preference_subscription_confirmation':False
                    }
            self.write(vals)
