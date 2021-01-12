# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Lead(models.Model):
    _inherit = 'crm.lead'

    event_id = fields.Many2one('event.event', 'Event')

    information_sharing = fields.Selection([('1_m', '1 Month'),
                                            ('3_m', '3 Months'),
                                            ('6_m', '6 Months'),
                                            ('1_y', '1 Year'),
                                            ('share_third',
                                             'We are currently sharing confidential documents with third parties.'),
                                            ('use_sharevault',
                                             'We currently use ShareVault.'),
                                            ('dont_sharevault',
                                             'We dont use ShareVault, but we are currently sharing confidential documentation with third parties.'),
                                            ], 'Information Sharing', store=True)

    # Initially, we needed to save this in order to send a confirmation email afterwards
    # but, after changes required by SV, we now keep it, in order to have a relation
    # between the lead and the shared link used
    typ_id = fields.Many2one('web.thankyou.pages','Thank You Message')

    share_link_id = fields.Many2one('documents.share', 'Shared Link')

    #tracked_link_id = fields.Many2one('link.tracker', 'Tracked link')


    questions_comments = fields.Text('Questions/Comments')
    sharevault_name = fields.Char('Name of ShareVault')
    accept_msa = fields.Boolean("I have read and agree to the ShareVault MSA.")
    industry = fields.Selection([
                    ('advertising_marketing','Advertising & Marketing'),
                    ('agriculture','Agriculture'),
                    ('consulting_advisory','Consulting & Advisory'),
                    ('education','Education'),
                    ('energy / Resources','Energy / Resources'),
                    ('entertainment','Entertainment'),
                    ('finance','Finance'),
                    ('government','Government'),
                    ('hospitality','Hospitality'),
                    ('legal','Legal'),
                    ('life Sciences','Life Sciences'),
                    ('manufacturing' ,'Manufacturing'),
                    ('not for Profit' ,'Not for Profit'),
                    ('other' ,'Other'),
                    ('real Estate / Construction', 'Real Estate / Construction'),
                    ('technology', 'Technology'),
                    ('retail', 'Retail'),
                    ('transportation', 'Transportation'),
                    ('unable-To-Locate', 'Unable-To-Locate'),
                    ('cannabis', 'Cannabis')
                    ], string='Industry')


class MqlType(models.Model):
    _name = 'mql.type'
    _description = 'MQL Type for website form'

    name = fields.Char('MQL Type')