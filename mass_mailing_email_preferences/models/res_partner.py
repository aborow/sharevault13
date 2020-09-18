# -*- coding: utf-8 -*-
from odoo import api, fields, models, _,tools
import hashlib
import hmac
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    """
    def _get_partner_unsubscribe_url(self):
        for partner_rec in self:
            if partner_rec.email:
                email = partner_rec.email
                secret = self.env["ir.config_parameter"].sudo().get_param("database.secret")
                url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
                token = (self.env.cr.dbname, tools.ustr(email))
                result = hmac.new(secret.encode('utf-8'), repr(token).encode('utf-8'), hashlib.sha512).hexdigest()
                email = email.replace('@', '%40')
                finalurl = url + '/update/contact?email=' + email + '&token=' + result
                partner_rec.email_unsubscribe_url = finalurl
            else:
                partner_rec.email_unsubscribe_url = False

    email_unsubscribe_url = fields.Char(compute='_get_partner_unsubscribe_url', string='Mail Subscribe URL')
    """

    def unsubscribe_url(self):
        return "/update/contact/email=%s&token=%s" % (self.email, self.generate_token())

    def generate_token(self, email=False):
        if not email:
            email = self.email
        secret = self.env["ir.config_parameter"].sudo().get_param("database.secret")
        token = (self.env.cr.dbname, tools.ustr(email))
        result = hmac.new(secret.encode('utf-8'), repr(token).encode('utf-8'), hashlib.sha512).hexdigest()
        return result


    email_preference_marketing = fields.Boolean('Marketing Updates', default=True, help='Marketing offers and updates')
    email_preference_white_papers = fields.Boolean('White Papers and Infographic', default=True, help='Relevant Industry news, resources and information')
    email_preference_events = fields.Boolean('Events and Webinars', default=True, help='Relevant Industry events and thought leadership')
    email_preference_blog = fields.Boolean('Blog Subscription', default=True, help='Timely updates with the latest blog posts')
    email_preference_company_news = fields.Boolean('Company News & Updates', default=True, help='News and Information related to ShareVault')
    email_preference_product_news = fields.Boolean('Product News & Updates', default=True, help='ShareVault news and product updates')

    @api.onchange(
                    'email_preference_marketing', 'email_preference_white_papers',
                    'email_preference_events', 'email_preference_blog',
                    'email_preference_company_news', 'email_preference_product_news'
                    )
    def onchange_email_preferences(self):
        if any([
                self.email_preference_marketing,
                self.email_preference_white_papers,
                self.email_preference_events,
                self.email_preference_blog,
                self.email_preference_company_news,
                self.email_preference_product_news
                ]
            ):
            self.opt_out = False


    @api.onchange('opt_out')
    def onchange_opt_out(self):
        if self.opt_out:
            vals = {
                    'email_preference_marketing':False,
                    'email_preference_white_papers':False,
                    'email_preference_events':False,
                    'email_preference_blog':False,
                    'email_preference_company_news':False,
                    'email_preference_product_news':False
                    }
            self.write(vals)
