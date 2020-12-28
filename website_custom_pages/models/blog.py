# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError

class BlogPost(models.Model):
    _inherit = 'blog.post'

    webpage_id = fields.Many2one('website.page', 'Page',
                            help="Set your own URL to override Odoo's default")

    """
    @api.onchange('custom_url')
    @api.depends('custom_url')
    def build_custom_url(self):
        if self.custom_url:
            aux = self.custom_url.replace('\\','/').replace('//','/')\
                        .replace(' ','-').lower()
            if not aux.startswith('/'):
                aux = '/' + aux
            #aux = self.custom_url.split('/')
            #if aux[0] == '':
            #    del aux[0]
            #if aux[0] != 'o':
            #    aux.insert(0, 'o')
            #aux = '/'.join(aux)
            self.custom_url = aux
    """
    @api.constrains('webpage_id')
    def check_webpage_id(self):
        for s in self:
            if s.webpage_id:
                if self.env['blog.post']\
                        .search_count([
                                        ('webpage_id','=',s.webpage_id.id),
                                        ('blog_id','=',s.blog_id.id),
                                        ('id','!=',s.id)
                                        ]):
                    raise ValidationError('The association between a blog post and a page should be unique')
