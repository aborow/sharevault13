# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    email_preference_confirmation = fields.Boolean('Confirmation Email', default=True)
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
