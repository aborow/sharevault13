# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
#from odoo.exceptions import ValidationError

#import logging
#_logger = logging.getLogger(__name__)

class Lead(models.Model):
    _inherit = 'crm.lead'

    sharevault_id = fields.Many2one('sharevault.sharevault','ShareVault')

    mql_date = fields.Char('MQL Date')
    mql_recycle_counter = fields.Integer('MQL Recycle counter')
    mql_recycle_store = fields.Integer('MQL Recycle score')
    mql_type = fields.Selection([('scorein','ScoreIn'),
                                 ('pff','PFF'),
                                 ('contentnibbler','ContentNibbler'),
                                 ('adhoc','Adhoc'),
                                 ('chat','Chat'),], 'MQL Type')
    mql_type_date = fields.Date('MQL Type Date')
    marketing_note = fields.Char('Marketing note')
    original_source = fields.Char('Original Source')
    recycled = fields.Boolean('Recycled')


    """
    lead_id

    crm.lead
    	> sharevault_id


    add smart button on ther contacts (same record and dependents)
    list
    """
