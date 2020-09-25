# -*- coding: utf-8 -*-
from odoo import models, fields,api, _
import base64
import io
import xlsxwriter
from odoo.exceptions import Warning,ValidationError


class WebThankYouPages(models.Model):
    _name = "web.thankyou.pages"
    _description = "Thank you Pages on sharevault website form"

    name = fields.Char('Name')
    text = fields.Html('Text')
    active = fields.Boolean('Active')