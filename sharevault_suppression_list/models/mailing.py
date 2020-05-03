# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

# No edit will be allowed to make things easier
# If someone want to change the domain, he shoud delete it and create a new one
class MailingSuppressionList(models.Model):
    _name = 'mail.suppression_list'
    _description = 'Domain Supression List for Emailing'

    name = fields.Char('Domain')


    # add, go through all the contacts with an email like "domain" and blacklist them
    # delete, go through all the contacts with an email like "domain" and UNblacklist them
