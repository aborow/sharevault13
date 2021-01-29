import json
import logging
import requests
from odoo import api, fields, models
from odoo.exceptions import Warning
from datetime import date
from datetime import timedelta

_logger = logging.getLogger(__name__)

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

# MQL Type
MQL_TYPE = [('scorein', 'ScoreIn'),
            ('pff', 'PFF'),
            ('contentnibbler', 'ContentNibbler'),
            ('adhoc', 'Adhoc'),
            ('chat', 'Chat')]

# Lead Type
Lead_Type = [('new', 'New Lead'),
             ('sub', 'Subscriber'),
             ('sales_ql', 'Sales Qualified Lead'),
             ('marketing_ql', 'Marketing Qualified Lead')]


def _log_logging(env, message, function_name, path):
    env['ir.logging'].sudo().create({
        'name': 'Salesforce Lead Sync',
        'type': 'server',
        'level': 'info',
        'dbname': env.cr.dbname,
        'message': message,
        'func': function_name,
        'path': path,
        'line': '0',
    })

class SyncLeadWizard(models.TransientModel):
    _name = 'sync.lead.wizard'
    _description = "Sync Lead from SalesForce"

    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)

    def fetch_sf_lead_details(self, rec):
        res_company_obj = self.env['res.company'].search([('id', '=', self._context.get('active_id') or 1)])
        if res_company_obj.sf_access_token:
            headers = {}
            headers['Authorization'] = 'Bearer ' + str(res_company_obj.sf_access_token)
            headers['accept'] = 'application/json'
            headers['Content-Type'] = 'text/plain'
            data = requests.request('GET', res_company_obj.sf_url + "/services/data/v40.0/sobjects/Lead/" + str(rec),
                                    headers=headers)
            if data.status_code == 200:
                if data.text:
                    leads_data = json.loads(str(data.text))
                    return leads_data
            else:
                return False

    def create_lead(self, lead_dict, sf_id):
        res_company_obj = self.env['res.company'].search([('id', '=', self._context.get('active_id') or 1)])
        lead_obj = self.env['crm.lead']
        headers = {}
        headers['Authorization'] = 'Bearer ' + str(res_company_obj.sf_access_token)
        headers['accept'] = 'application/json'
        headers['Content-Type'] = 'text/plain'
        lead_exists = lead_obj.search([('x_salesforce_id', '=', sf_id)])
        if not lead_exists:
            if lead_dict:
                lead_dict['salesforce_response'] = ''
                res = lead_obj.create(lead_dict)
                if res:
                    ''' Write x_salesforce_id '''
                    res.write(
                        {'x_salesforce_id': sf_id, 'is_sf_lead': True, 'sf_last_sync_date': fields.Datetime.now()})
                    return res
                else:
                    return False
            else:
                return False
        if lead_exists:
            if lead_dict:
                lead_dict['x_salesforce_id'] = sf_id
                lead_dict['is_sf_lead'] = True
                lead_dict['sf_last_sync_date'] = fields.Datetime.now()
                lead_dict['salesforce_response'] = ''
                lead_exists.write(lead_dict)
                return lead_exists
            else:
                return False

    def prepare_dict(self, rec, lead_read):
        lead_dict = {}
        ''' PREPARE DICT FOR INSERTING IN Leads '''
        if rec[1]:
            users_obj = self.env['res.users'].search([('name', '=', rec[1])],
                                                     limit=1)
            lead_dict['user_id'] = users_obj.id
        if lead_read.get('Status'):
            stage_obj = self.env['crm.stage'].search(
                [('name', '=', lead_read.get('Status')), ('is_lead_stage', '=', True)],
                limit=1)
            lead_dict['stage_id'] = stage_obj.id
        if lead_read.get('Name'):
            lead_dict['name'] = lead_read.get('Name')
            lead_dict['contact_name'] = lead_read.get('Name')
        if lead_read.get('Title'):
            title_obj = self.env['res.partner.title'].search([('name', '=', lead_read.get('Title'))], limit=1)
            if title_obj:
                lead_dict['title'] = title_obj.id
            else:
                title_obj = self.env['res.partner.title']
                title_res = title_obj.create(
                    {'name': lead_read.get('Title'), 'shortcut': lead_read.get('Title')})
                if title_res:
                    lead_dict['title'] = title_res.id
        if lead_read.get('Phone'):
            lead_dict['phone'] = lead_read.get('Phone')
        if lead_read.get('Email'):
            lead_dict['email_from'] = lead_read.get('Email')
        if lead_read.get('FrontSpin_Control__c'):
            lead_dict['phone'] = lead_read.get('Phone')
        if lead_read.get('DoNotCall'):
            lead_dict['do_not_call'] = lead_read.get('DoNotCall')
        if lead_read.get('HasOptedOutOfEmail'):
            lead_dict['email_opt_out'] = lead_read.get('HasOptedOutOfEmail')
        if lead_read.get('Industry'):
            for ind in INDUSTRY:
                if ind[1] == lead_read.get('Industry'):
                    lead_dict["industry"] = str(ind[0])
        if lead_read.get('FrontSpin_Control__c'):
            for mt in MQL_TYPE:
                if mt[1] == lead_read.get('FrontSpin_Control__c'):
                    lead_dict["mql_type"] = str(mt[0])
        if lead_read.get('Lead_Type__c'):
            if lead_read.get('Lead_Type__c') == 'MQL':
                lead_dict["lead_type"] = 'marketing_ql'
        if lead_read.get('MQL_Type_Date__c'):
            lead_dict["mql_type_date"] = lead_read.get('MQL_Type_Date__c')
        if lead_read.get('LastModifiedDate'):
            lm_date = lead_read.get('LastModifiedDate')
            lm_date_time = lm_date.split('T')[0] + " " + lm_date.split('T')[1].split('.')[0]
            lead_dict['sf_last_modified_date'] = lm_date_time
        if lead_read.get('Form_Name__c'):
            source_obj = self.env['utm.source'].search(
                [('name', '=', lead_read.get('Form_Name__c'))], limit=1)
            if source_obj:
                lead_dict['source_id'] = source_obj.id
            else:
                source_obj = self.env['utm.source']
                source_res = source_obj.create({'name': lead_read.get('Form_Name__c')})
                if source_res:
                    lead_dict['source_id'] = source_res.id
        if lead_dict:
            return self.create_lead(lead_dict, lead_read.get('Id'))

    def import_leads(self):
        try:
            sync_by = "manual"
            self.sync_lead_from_sfcd(sync_by)
        except Exception as e:
            raise Warning("Oops Some error Occured" + str(e))

    @api.model
    def sync_lead_from_sfcd(self, sync_by):
        start_date = date.today()
        end_date = start_date - timedelta(days=1)
        try:
            res_company_obj = self.env['res.company'].search([('id', '=', 1)])
            if res_company_obj.sf_access_token:
                headers = {}
                headers['Authorization'] = 'Bearer ' + str(res_company_obj.sf_access_token)
                headers['accept'] = 'application/json'
                headers['Content-Type'] = 'text/plain'
                data = ''
                if sync_by == "create_date":
                    data = requests.request('GET',
                                            res_company_obj.sf_url + "/services/data/v40.0/query/?q=select Id,"
                                                                     "Owner.Name from Lead where CreatedDate >= "
                                                                     "%sT00:00:00Z AND CreatedDate <= %sT23:59:59Z" % (
                                                str(end_date), str(start_date)),
                                            headers=headers)
                if sync_by == "modified_date":
                    data = requests.request('GET',
                                            res_company_obj.sf_url + "/services/data/v40.0/query/?q=select Id,"
                                                                     "Owner.Name from Lead where LastModifiedDate >= "
                                                                     "%sT00:00:00Z AND LastModifiedDate <= "
                                                                     "%sT23:59:59Z" % (
                                                str(end_date), str(start_date)),
                                            headers=headers)
                if sync_by == "manual":
                    data = requests.request('GET',
                                            res_company_obj.sf_url + "/services/data/v40.0/query/?q=select Id,"
                                                                     "Owner.Name from Lead where CreatedDate >= "
                                                                     "%sT00:00:00Z AND CreatedDate <= %sT23:59:59Z" % (
                                                str(self.start_date), str(self.end_date)),
                                            headers=headers)
                if data != '':
                    recs = []
                    parsed_result = data.json()
                    parsed_data = json.loads(str(data.text))
                    if parsed_data:
                        for p in parsed_data.get('records'):
                            recs.append([p.get('Id'), p.get('Owner').get('Name')])
                    for rec in recs:
                        lead_read = self.fetch_sf_lead_details(rec[0])
                        lead = self.prepare_dict(rec, lead_read)
                        _log_logging(self.env, "ID: %s Email: %s Response from SF: %s" % (
                        str(lead.id), str(lead.email_from), str(parsed_result)), "sync_lead_from_sfcd", sync_by)

        except Exception as e:
            _log_logging(self.env,
                         str('Oops Some error Occured'),
                         "sync_lead_from_sfcd", sync_by)
            raise Warning("Oops Some error Occured" + str(e))
