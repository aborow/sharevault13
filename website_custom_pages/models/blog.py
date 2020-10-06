# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError

class BlogPost(models.Model):
    _inherit = 'blog.post'

    custom_url = fields.Char('Custom URL',
                            help="Set your own URL to override Odoo's default")

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

    @api.constrains('custom_url')
    def check_custom_url(self):
        for s in self:
            if s.custom_url:
                if self.env['blog.post']\
                        .search_count([
                                        ('custom_url','=',s.custom_url),
                                        ('id','!=',s.id)
                                        ]):
                    raise ValidationError('Custom URL must be unique')
