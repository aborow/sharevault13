# -*- coding: utf-8 -*-
from odoo import api, fields, models

class WebPageCreateWizard(models.TransientModel):
    _name = 'website.page.create_wizard'
    _description = 'Wizard to create a page out of a template'

    page_template_id = fields.Many2one('website.page', 'Template', required=True)
    website_id = fields.Many2one('website', 'Website',
                                    related='page_template_id.website_id')
    name = fields.Char('Name', required=True)
    url = fields.Char('Page URL', required=True)
    blog_id = fields.Many2one('blog.blog', 'Blog', required=True)
    blog_post_id = fields.Many2one('blog.post', 'Blog Post',
                                    domain="[('webpage_id','=',False)]")


    def action_create_page(self):
        # Step 1 - we create a page
        new_page_id = self.page_template_id.copy()
        if new_page_id:
            # we must change the 'key' of the view, otherwise, any changes will
            # be made into the original view
            new_page_id.view_id.key = 'website.%s' %  new_page_id.view_id.id
            new_page_id.write({
                                'name': self.name,
                                'url': self.url,
                                'website_id': self.website_id\
                                                and self.website_id.id or False
                                })

            # Step 2 - we create a blog entry to "load" the new page
            if not self.blog_post_id:
                self.env['blog.post'].create({
                                            'website_id': self.website_id.id,
                                            'blog_id': self.blog_id.id,
                                            'name': self.name,
                                            'webpage_id': new_page_id.id
                                            })

            # Step 3 - we redirect to the page, in edit mode
            return {
                    'type': 'ir.actions.act_url',
                    'url': self.url
                    }
