# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

#2.2) Buttons to call wizard (page URL / blog_post_id) - redirects to page edit


class WebPage(models.Model):
    _inherit = 'website.page'

    is_template = fields.Boolean('Is a template?', copy=False)

    def call_create_page_wizard(self):
        self.ensure_one()
        return {
                'type': 'ir.actions.act_window',
                'name': 'Create a page out of a template',
                'res_model': 'website.page.create_wizard',
                'target': 'new',
                'view_mode': 'form',
                'context': {'default_page_template_id': self.id}
                }


class WebPageCreateWizard(models.TransientModel):
    _name = 'website.page.create_wizard'
    _description = 'Wizard to create a page out of a template'

    page_template_id = fields.Many2one('website.page', 'Template')
    page_url = fields.Char('Page URL')
    blog_post_id = fields.Many2one('blog.post', 'Blog Post',
                                    domain="[('webpage_id','=',False)]")
