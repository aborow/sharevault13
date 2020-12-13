# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import ValidationError
import json
import logging
from datetime import datetime
import requests
_logger = logging.getLogger(__name__)

# Product- should create salesforce lead, Content - does not create a lead in salesforce
SOURCE_TYPE = [('product', 'Product'), ('content', 'Content')]

# Industry
INDUSTRY = [
    ('advertising_marketing', 'Advertising & Marketing'),
    ('agriculture', 'Agriculture'),
    ('consulting_advisory', 'Consulting & Advisory'),
    ('education', 'Education'),
    ('energy / Resources', 'Energy / Resources'),
    ('entertainment', 'Entertainment'),
    ('finance', 'Finance'),
    ('government', 'Government'),
    ('hospitality', 'Hospitality'),
    ('legal', 'Legal'),
    ('life Sciences', 'Life Sciences'),
    ('manufacturing', 'Manufacturing'),
    ('not for Profit', 'Not for Profit'),
    ('other', 'Other'),
    ('real Estate / Construction', 'Real Estate / Construction'),
    ('technology', 'Technology'),
    ('retail', 'Retail'),
    ('transportation', 'Transportation'),
    ('unable-To-Locate', 'Unable-To-Locate'),
    ('cannabis', 'Cannabis')
]

class CrmLead(models.Model):
    _inherit = "crm.lead"

    def _default_team_id(self, user_id):
        domain = [('use_leads', '=', True)] if self._context.get('default_type') == "lead" or self.type == 'lead' else [
            ('use_opportunities', '=', True)]
        return self.env['crm.team']._get_default_team_id(user_id=user_id, domain=domain)

    def _default_stage_id(self):
        team = self._default_team_id(user_id=self.env.uid)
        return self._stage_find(team_id=team.id, domain=[('fold', '=', False)]).id

    lead_type = fields.Selection([('new', 'New Lead'),
                                  ('sub', 'Subscriber'),
                                  ('sales_ql', 'Sales Qualified Lead'),
                                  ('marketing_ql', 'Marketing Qualified Lead')], string="Lead Type", default="new")
    stage_id = fields.Many2one('crm.stage', string='Stage', ondelete='restrict', tracking=True, index=True, copy=False,
                               domain="['|', ('team_id', '=', False), ('team_id', '=', team_id)]",
                               group_expand='_read_group_stage_ids', default=lambda self: self._default_stage_id())
    is_lead_stage = fields.Boolean(related='stage_id.is_lead_stage', string='Lead Stages')
    stage_ids = fields.Many2many('crm.stage', compute="_compute_stage_ids", string='Stages')

    european_union = fields.Boolean('Are you a citizen or resident of the European Union (EU)?')
    accept_conditions = fields.Boolean('Agree data collection', default=False)

    request_type = fields.Selection([
                                    ('sales_inquiry','Sales Inquiry'),
                                    ('support_inquiry','Support Inquiry'),
                                    ('partnership_inquiry','Partnership Inquiry'),
                                    ('other','Other'),
                                    ], string='Request Type')
    x_salesforce_id = fields.Char('SalesForce ID', copy=False)
    x_salesforce_exported = fields.Boolean('Exported To Salesforce', default=False, copy=False)
    x_is_updated = fields.Boolean('x_is_updated', default=False, copy=False)
    x_last_modified_on = fields.Datetime("SF last Modified.", copy=False)
    salesforce_response = fields.Text('Response')

    def write(self, vals):
        if vals:
            if 'x_last_modified_on' in vals.keys():
                if vals['x_last_modified_on']:
                    vals['x_is_updated'] = True
                else:
                    vals['x_is_updated'] = False
            else:
                vals['x_is_updated'] = False

        res = super(CrmLead, self).write(vals)
        return res

    def create_lead_sf_dict(self):
        sf_lead_dict = {}
        # sf_lead_dict["LastName"] = str(self.name)
        # sf_lead_dict["FirstName"] = str(self.name)
        name_split = self.name.split()
        sf_lead_dict["FirstName"] = name_split[0]
        if len(name_split) > 1:
            lastname = name_split[1::]
            sf_lead_dict["LastName"] = ' '.join(lastname)
        else:
            sf_lead_dict["LastName"] = "."
        if self.email_from:
            sf_lead_dict["Email"] = str(self.email_from)
        if self.partner_name:
            sf_lead_dict["Company"] = str(self.partner_name)
        if self.city:
            sf_lead_dict["City"] = str(self.city)
        if self.street:
            sf_lead_dict["Street"] = str(self.street)
        if self.state_id:
            sf_lead_dict["State"] = str(self.state_id.name)
        if self.phone:
            sf_lead_dict["Phone"] = str(self.phone)
        # if self.mobile:
        #     sf_lead_dict["MobilePhone"] = str(self.mobile)
        if self.zip:
            sf_lead_dict["PostalCode"] = str(self.zip)
        if self.country_id:
            sf_lead_dict["Country"] = str(self.country_id.name)
        if self.website:
            sf_lead_dict["Website"] = str(self.website)
        if self.lead_type:
            if self.lead_type == 'marketing_ql':
                sf_lead_dict["Lead_Type__c"] = 'MQL'
        sf_lead_dict["LeadSource"] = 'inbound marketing'
        sf_lead_dict["Lead_Source_Details__c"] = 'Odoo'
        if self.industry:
            for ind in INDUSTRY:
                if ind[0] == self.industry:
                    sf_lead_dict["Industry"] = str(ind[1])
        if self.source_id:
            sf_lead_dict['LeadSrcDescr__c'] = self.source_id.name
        if self.mql_type:
            if self.mql_type == 'scorein':
                sf_lead_dict["FrontSpin_Control__c"] = 'ScoreIn'
            if self.mql_type == 'pff':
                sf_lead_dict["FrontSpin_Control__c"] = 'PFF'
            if self.mql_type == 'contentnibbler':
                sf_lead_dict["FrontSpin_Control__c"] = 'ContentNibbler'
            if self.mql_type == 'adhoc':
                sf_lead_dict["FrontSpin_Control__c"] = 'Adhoc'
            if self.mql_type == 'chat':
                sf_lead_dict["FrontSpin_Control__c"] = 'Chat'
        if self.mql_type_date:
            sf_lead_dict["MQL_Type_Date__c"] = str(self.mql_type_date)
        return sf_lead_dict

    def create_lead_in_sf(self, sf_partner_dict):
        create_in_sf = True
        sf_config = self.env.user.company_id
        if not sf_config.sf_access_token:
            return False
        headers = sf_config.get_headers(True)

        endpoint = '/services/data/v40.0/sobjects/Lead'
        parsed_dict = json.dumps(sf_partner_dict)
        result = requests.request('POST', sf_config.sf_url + endpoint, headers=headers, data=parsed_dict)
        if result.status_code in [200, 201]:
            parsed_result = result.json()
            self.salesforce_response = 'Successfully Created'
            if parsed_result.get('id'):
                self.x_is_updated = True
                self.x_salesforce_exported = True
                self.x_last_modified_on = datetime.now()
                self.x_salesforce_id = parsed_result.get('id')
                return parsed_result.get('id')
            else:
                return False
        elif result.status_code == 401:
            sf_config.refresh_token_from_access_token()
            self.salesforce_response = 'ACCESS TOKEN EXPIRED, GETTING NEW REFRESH TOKEN...'
            _logger.info("ACCESS TOKEN EXPIRED, GETTING NEW REFRESH TOKEN...")
            return False
        else:
            parsed_json = result.json()
            _logger.error('response Of Partner creation in salesforce  (%s)', str(parsed_json[0].get('message')))
            self.salesforce_response = str(parsed_json[0].get('message'))
            return False

    def create_lead_sf(self):
        for lead in self.browse(self.id):
            if not lead.x_salesforce_exported:
                sf_lead_dict = lead.create_lead_sf_dict()
                lead.create_lead_in_sf(sf_lead_dict)
    @api.model
    def create_sf_lead(self):
        if self._context.get('website_id'):
            for rec in self:
                if rec.source_id:
                    if rec.source_id.source_type == 'product':
                        rec.create_lead_sf()
                        now = datetime.now()
                        rec.mql_date = now.strftime("%m/%d/%Y %H:%M:%S")
                        rec.lead_type = 'marketing_ql'

    def sync_manual(self):
        self.create_lead_sf()
        now = datetime.now()
        self.mql_date = now.strftime("%m/%d/%Y %H:%M:%S")
        self.lead_type = 'marketing_ql'

    @api.model
    def assign_contact_lead(self):
        for rec in self:
            if rec.type == 'lead' and rec.email_from and not rec.partner_id:
                contact_id = rec.env['res.partner'].search([('email', '=', rec.email_from)], limit=1)
                if contact_id:
                    rec.write({'partner_id': contact_id.id})
                else:
                    vals_contact = {
                        'name': rec.name if rec.name else False,
                        'email': rec.email_from if rec.email_from else False,
                        'website': rec.website if rec.website else False,
                        'street': rec.street if rec.street else False,
                        'street2': rec.street2 if rec.street2 else False,
                        'city': rec.city if rec.city else False,
                        'state_id': rec.state_id.id if rec.state_id else False,
                        'zip': rec.zip if rec.zip else False,
                        'phone': rec.phone if rec.phone else False,
                        'mobile': rec.mobile if rec.mobile else False,
                        'european_union': rec.european_union if rec.european_union else False,
                        'type': 'contact',
                    }
                    partner = rec.env['res.partner']
                    partner_id = partner.create(vals_contact)
                    rec.write({'partner_id': partner_id.id})

    @api.model
    def update_lead_stages(self):
        for rec in self.search([]):
            if rec.type == 'lead':
                if rec.lead_type == 'new' and rec.score >= 40:
                    stage = self.env['crm.stage'].search([('name', '=', 'Open')], limit=1)
                    rec.write({'stage_id': stage.id,
                               'lead_type': 'marketing_ql'})
        return True

    def update_lead_score(self):
        stage = self.env['crm.stage'].search([('is_recycle_stage', '=', True)], limit=1)
        if not stage:
            raise ValidationError(_('Contact to Administrator for set Recycle stage'))
        if stage:
            self.stage_id = stage.id
            self.score = 0.0
            msg = _('Score is Recycled and set to zero')
            self.message_post(body=msg)

    def update_recycle_lead_score(self):
        for rec in self:
            stage = rec.env['crm.stage'].search([('is_recycle_stage', '=', True)], limit=1)
            if not stage:
                raise ValidationError(_('Contact to Administrator for set Recycle stage'))
            if stage:
                rec.stage_id = stage.id
                rec.score = 0.0
                msg = _('Score is Recycled and set to zero')
                rec.message_post(body=msg)

    @api.depends('type', 'is_lead_stage')
    def _compute_stage_ids(self):
        for rec in self:
            if rec.type == 'lead':
                rec.stage_ids = self.env['crm.stage'].search([('is_lead_stage', '=', True)]).ids
            if rec.type == "opportunity":
                rec.stage_ids = self.env['crm.stage'].search([('is_lead_stage', '=', False)]).ids

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        # retrieve team_id from the context and write the domain
        # - ('id', 'in', stages.ids): add columns that should be present
        # - OR ('fold', '=', False): add default columns that are not folded
        # - OR ('team_ids', '=', team_id), ('fold', '=', False) if team_id: add team columns that are not folded
        team_id = self._context.get('default_team_id')
        type = self._context.get('default_type')
        if type == 'opportunity':
            all_opp_stages = self.env['crm.stage'].search([('is_lead_stage', '!=', True)])
            if team_id:
                search_domain = [('id', 'in', all_opp_stages.ids), '|', ('team_id', '=', False),
                                 ('team_id', '=', team_id)]
            else:
                search_domain = [('id', 'in', all_opp_stages.ids)]
        if type == 'lead':
            all_lead_stages = self.env['crm.stage'].search([('is_lead_stage', '=', True)])
            if team_id:
                search_domain = [('id', 'in', all_lead_stages.ids), '|', ('team_id', '=', False),
                                 ('team_id', '=', team_id)]
            else:
                search_domain = [('id', 'in', all_lead_stages.ids)]

            # search_domain = [('id','in',all_lead_stages.ids)]
        # perform search
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    def _stage_find(self, team_id=False, domain=None, order='sequence'):
        """ Determine the stage of the current lead with its teams, the given domain and the given team_id
            :param team_id
            :param domain : base search domain for stage
            :returns crm.stage recordset
        """
        # collect all team_ids by adding given one, and the ones related to the current leads
        team_ids = set()
        if team_id:
            team_ids.add(team_id)
        for lead in self:
            if lead.team_id:
                team_ids.add(lead.team_id.id)
        # generate the domain
        if team_ids:
            search_domain = ['|', ('team_id', '=', False), ('team_id', 'in', list(team_ids))]
        else:
            search_domain = [('team_id', '=', False)]
        # AND with the domain in parameter
        if domain:
            search_domain += list(domain)
        # perform search, return the first found
        if self._context.get('default_type') == 'lead':
            all_lead_stages = self.env['crm.stage'].search([('is_lead_stage', '=', True)])
            search_domain += [('id', 'in', all_lead_stages.ids)]
        if self._context.get('website_id'):
            all_lead_stages = self.env['crm.stage'].search([('is_lead_stage', '=', True)])
            search_domain += [('id', 'in', all_lead_stages.ids)]
        return self.env['crm.stage'].search(search_domain, order=order, limit=1)


class CrmStage(models.Model):
    _inherit = "crm.stage"

    is_lead_stage = fields.Boolean('Is Lead Stage?', default=False)
    is_recycle_stage = fields.Boolean('Is Recycle Stage', default=False)

    @api.constrains('is_recycle_stage')
    def _check_boolean(self):
        checked_bool = self.search([('id', '!=', self.id), ('is_recycle_stage', '=', True)], limit=1)
        if self.is_recycle_stage and checked_bool:
            raise ValidationError(_("There's already one checked boolean in record '%s'") % checked_bool.name)


class UtmSource(models.Model):
    _inherit = "utm.source"

    source_type = fields.Selection(SOURCE_TYPE, string="Source Type")