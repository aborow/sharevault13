# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
#from odoo.exceptions import ValidationError

#import logging
#_logger = logging.getLogger(__name__)

class Sharevault(models.Model):
    _name = 'sharevault.sharevault'
    _description = 'ShareVaults'

    sharevault_name = fields.Char('Name', required=True)
    key = fields.Integer('Key')
    #company_id = fields.Many2one('res.company', 'Company')
    company_id = fields.Many2one('res.partner', 'Company')
    sv_type = fields.Selection([('sv','SV'),('sve','SVe')], 'Type')
    sharevault_owner = fields.Many2one('res.partner', 'Owner')
    partner_id_title = fields.Char('Title', related='sharevault_owner.function')
    partner_id_email = fields.Char('Email', related='sharevault_owner.email')
    partner_id_phone = fields.Char('Phone', related='sharevault_owner.phone')
    sv_creation_dt = fields.Date('Creation')
    sv_expiration_dt = fields.Date('Expiration')
    dt_last_upload = fields.Date('Last upload')
    dt_last_download = fields.Date('Last download')
    dt_last_login = fields.Date('Last login')
    term_start_date = fields.Date('Term Start Date')
    term_end_date = fields.Date('Term End Date')
    quota_pages = fields.Integer('Quota: pages')
    quota_users = fields.Integer('Quota: users')
    quota_mb = fields.Integer('Quota: MB')
    util_pages = fields.Float('Utilized: pages')
    util_users = fields.Float('Utilized: users')
    util_mb = fields.Float('Utilized: MB')
    total_logins = fields.Integer('Total: logins')
    total_tags = fields.Integer('Total: tags')
    total_tag_value = fields.Integer('Total: tag value')
    total_groups = fields.Integer('Total: groups')
    uncounted_filesize_mb = fields.Float('Uncounted filesize (MB)')
    locked_unlocked = fields.Selection([('locked', "Locked"),
                               ('unlocked', "Unlocked")],
                              string="Locked", default='unlocked')
    published_last_30_days_mb = fields.Float('Published in the last 30 days (MB)')
    lead_id = fields.Many2one('crm.lead', 'Opportunity')
    title = fields.Char('Contact Title')
    contact_email = fields.Char('Contact Email')
    contact_phone = fields.Char('Contact Phone')
    sharevault_id = fields.Char('Sharevault ID', required=True)
