# -*- coding: utf-8 -*-
import uuid

from odoo import api, fields, models, tools, _

class Partner(models.Model):
    _inherit = 'res.partner'

    company_type =  fields.Selection(string='Contact Type')

    hs_company_id = fields.Char("HS Company ID")
    hs_create_date = fields.Date("HS Create Date")
    hs_last_modified_date = fields.Date("HS Last Modified Date")
    hs_lastupdated = fields.Date("HS LastUpdated")
    hs_first_contact_create_date = fields.Date("HS First Contact Create Date")
    hs_first_deal_created_date = fields.Date("HS First Deal Created Date")
    hs_lead_status = fields.Char("HS Lead Status")
    hs_subscription_status = fields.Char("HS Subscription Status")
    hs_bio_convention_status = fields.Char("HS BIO Convention Status")
    hs_company_owner = fields.Char("HS Company owner")
    hs_owner_assigned_date = fields.Date("HS Owner Assigned Date")
    hs_number_of_blockers = fields.Char("HS Number of blockers")
    hs_number_of_contacts_with_a_buying_role = fields.Char("HS Number of contacts with a buying role")
    hs_number_of_decision_makers = fields.Char("HS Number of decision makers")
    hs_number_of_open_deals = fields.Char("HS Number of open deals")
    hs_number_of_times_contacted = fields.Char("HS Number of times contacted")
    hs_number_of_pageviews = fields.Char("HS Number of Pageviews")
    hs_number_of_sessions = fields.Char("HS Number of Sessions")
    hs_number_of_form_submissions = fields.Char("HS Number of Form Submissions")
    hs_time_of_first_session = fields.Char("HS Time of First Session")
    hs_first_touch_converting_campaign = fields.Char("HS First Touch Converting Campaign")
    hs_first_conversion = fields.Char("HS First Conversion")
    hs_first_conversion_date = fields.Date("HS First Conversion Date")
    hs_last_activity_date = fields.Date("HS Last Activity Date")
    hs_last_sales_activity_date = fields.Date("HS Last Sales Activity Date")
    hs_last_open_task_date = fields.Date("HS Last Open Task Date")
    hs_last_logged_call_date = fields.Date("HS Last Logged Call Date")
    hs_last_contacted = fields.Date("HS Last Contacted")
    hs_last_booked_meeting_date = fields.Date("HS Last Booked Meeting Date")
    hs_time_last_seen = fields.Date("HS Time Last Seen")
    hs_last_touch_converting_campaign = fields.Char("HS Last Touch Converting Campaign")
    hs_lead_source = fields.Char("HS Lead Source")
    hs_lead_source_description = fields.Char("HS Lead Source Description")
    hs_opportunity_stage = fields.Char("HS Opportunity Stage")
    hs_became_an_other_lifecycle_date = fields.Date("HS Became an Other Lifecycle Date")
    hs_became_a_subscriber_date = fields.Date("HS Became a Subscriber Date")
    hs_became_a_lead_date = fields.Date("HS Became a Lead Date")
    hs_became_a_marketing_qualified_lead_date = fields.Date("HS Became a Marketing Qualified Lead Date")
    hs_became_a_sales_qualified_lead_date = fields.Date("HS Became a Sales Qualified Lead Date")
    hs_became_an_opportunity_date = fields.Date("HS Became an Opportunity Date")
    hs_became_a_customer_date = fields.Date("HS Became a Customer Date")
    hs_became_an_evangelist_date = fields.Date("HS Became an Evangelist Date")
    hs_first_deal_created_date = fields.Date("HS First Deal Created Date")
    hs_associated_contacts = fields.Char("HS Associated Contacts")
    hs_associated_deals = fields.Char("HS Associated Deals")
    hs_total_open_deal_value = fields.Char("HS Total open deal value")
    hs_associated_company_id = fields.Char("HS Associated Company ID")
    hs_associated_company = fields.Char("HS Associated Company")
    hs_associated_contacts = fields.Char("HS Associated Contacts")
    hs_account_status = fields.Char("HS Account Status")
    hscontact_region = fields.Char("HScontact Region")
    hs_contact_id = fields.Integer("HS Contact ID")
    hs_marketing_emails_bounced = fields.Integer("HS Marketing emails bounced")
    hs_marketing_emails_delivered = fields.Integer("HS Marketing emails delivered")
    hs_marketing_emails_opened = fields.Integer("HS Marketing emails opened")
    hs_marketing_emails_clicked = fields.Integer("HS Marketing emails clicked")
    hs_email_hard_bounce_reason = fields.Char("HS Email hard bounce reason")
    hs_forced_sync_to_sfdc = fields.Boolean("HS Forced Sync to SFDC")
    hs_contact_owner = fields.Char("HS Contact owner")
    hs_original_source = fields.Char("HS Original Source")
    hs_original_source_drill_down_1 = fields.Char("HS Original Source Drill-Down 1")
    hs_original_source_drill_down_2 = fields.Char("HS Original Source Drill-Down 2")
    hs_recycled_flag_marketing = fields.Boolean("HS Recycled flag (Marketing)")
    hs_unqualified_reason = fields.Char("HS Unqualified Reason")
    hs_no_sales_calls = fields.Boolean("HS No Sales Calls")
    hs_affiliations = fields.Char("HS Affiliations")
    hs_affiliate_contact = fields.Char("HS Affiliate Contact")
    hs_regional_affiliate = fields.Char("HS Regional Affiliate")
    hs_predictive_lead_score = fields.Char("HS Predictive Lead Score")
    hs_lifecycle_stage = fields.Char("HS Lifecycle Stage")
    hs_mql_type = fields.Char("HS MQL Type")
    hs_mql_type_date = fields.Date("HS MQL Type Date")
    hs_mql_date = fields.Date("HS MQL Date")
    hs_lead_rating = fields.Char("HS Lead Rating")
    hs_i_agree_to_the_msa = fields.Char("HS I agree to the MSA")
    hs_recent_conversion = fields.Char("HS Recent Conversion")
    hs_recent_conversion_date = fields.Char("HS Recent Conversion Date")
    hs_time_first_seen = fields.Date("HS Time First Seen")
    hs_sends_since_last_engagement = fields.Integer("HS Sends Since Last Engagement")
    hs_time_of_last_session = fields.Date("HS Time of Last Session")
    hs_average_pageviews = fields.Char("HS Average Pageviews")
    hs_first_page_seen = fields.Char("HS First Page Seen")
    hs_last_page_seen = fields.Char("HS Last Page Seen")
    hs_number_of_event_completions = fields.Integer("HS Number of event completions")
    hs_number_of_unique_forms_submitted = fields.Integer("HS Number of Unique Forms Submitted")
    hs_total_number_of_zoom_webinar_registrations = fields.Integer("HS Total number of Zoom webinar registrations")
    hs_total_number_of_zoom_webinars_attended = fields.Integer("HS Total number of Zoom webinars attended")
    hs_last_registered_zoom_webinar = fields.Char("HS Last registered Zoom webinar")
    hs_average_zoom_webinar_attendance_duration = fields.Char("HS Average Zoom webinar attendance duration")
    hs_linkedin_clicks = fields.Integer("HS LinkedIn Clicks")
    hs_twitter_clicks = fields.Integer("HS Twitter Clicks")
    hs_facebook_clicks = fields.Integer("HS Facebook Clicks")
    hs_google_plus_clicks = fields.Integer("HS Google Plus Clicks")
    hs_broadcast_clicks = fields.Integer("HS Broadcast Clicks")
    hs_number_of_sales_activities = fields.Integer("HS Number of Sales Activities")
    hs_associated_company = fields.Char("HS Associated Company")
    hubspot_score = fields.Integer("HubSpot Score")
    sv_role = fields.Char("SV Role")
    zoomcontactid = fields.Char("ZoomContactID")
    linkedin_source = fields.Char("LinkedIn Source")
    linkedin_bio = fields.Char("LinkedIn Bio")
    linkedin_connections = fields.Char("LinkedIn Connections")
    twitter_username = fields.Char("Twitter Username")
    twitter_bio = fields.Char("Twitter Bio")
    twitter_profile_photo = fields.Char("Twitter Profile Photo")
    follower_count = fields.Char("Follower Count")
    klout_score = fields.Char("Klout Score")
    interested_learning = fields.Boolean(string="I'm interested in learning how to share our documents securely with external parties.")
    salesforce_campaign_ids = fields.Char("Salesforce Campaign IDs")
    department = fields.Char("Department")
    company_email_domain_name = fields.Char("Company Email Domain Name")
    company_news = fields.Char("Company News")
    sub_sub_industry = fields.Char("Sub Sub Industry")
    sic_description = fields.Char("SIC Description")
    naics_description = fields.Char("NAICS Description")
    duns_number = fields.Char("D-U-N-S Number")
    ip_address = fields.Char("IP Address")
    ip_city = fields.Char("IP City")
    ip_state_region = fields.Char("IP State/Region")
    ip_state_region_code = fields.Char("IP State Code/Region Code")
    ip_country = fields.Char("IP Country")
    ip_country_code = fields.Char("IP Country Code")
    ip_timezone = fields.Char("IP Timezone")
    year_founded = fields.Char("Year Founded")
    employees = fields.Char("Employees")
    annual_revenue = fields.Char("Annual Revenue")
    total_revenue = fields.Char("Total Revenue")
    ownership = fields.Char("Ownership")
    ticker = fields.Char("Ticker")
    market_capitalization_millions = fields.Char("Market Capitalization Millions")
    total_money_raised = fields.Char("Total Money Raised")
    last_funding_round = fields.Char("Last Funding Round")
    using_sharepoint = fields.Char("Using SharePoint")
    sharepoint_version = fields.Char("SharePoint Version")
    currently_with_competitor = fields.Char("Currently With Competitor")
    competitor_expiration_date = fields.Date("Competitor Expiration Date")
    indications = fields.Char("Indications")
    primary_therapy_areas = fields.Char("Primary Therapy Areas")
    secondary_therapy_areas = fields.Char("Secondary Therapy Areas")
    sub_sector = fields.Char("Sub-Sector")
    product_area = fields.Char("Product Area")
    products_managed = fields.Char("Products Managed")
    primary_product = fields.Char("Primary Product")
    dev_phase = fields.Char("Dev Phase")
    products_in_dev = fields.Char("Products In Dev")
    number_of_products_in_development = fields.Char("Number of Products in Development")
    products_on_market = fields.Char("Products on Market")
    number_of_products_on_the_market = fields.Char("Number of Products on the Market")
    licensing_status = fields.Char("Licensing Status")
    assetname = fields.Char("AssetName")
    assettype = fields.Char("AssetType")
    linkedin_company_page = fields.Char("LinkedIn Company Page")
    facebook_company_page = fields.Char("Facebook Company Page")
    use_technology_share_documents = fields.Char("Do you currently use a technology solution to share confidential documents with third parties?")
    how_many_deals = fields.Char("How many M&A deals is your organization likely to be involved in during the next twelve months?")
    msa_agreement = fields.Boolean("MSA Agreement")
    sharevault_usage_begin_date = fields.Date("ShareVault Usage Begin Date")
    data_last_updated = fields.Date("Data Last Updated")
    salesforce_account_id = fields.Char("Salesforce Account ID")
    hs_company_region = fields.Char("HS Company Region")



    # Making mailings available in Contacts - START
    def _get_mailing_counter(self):
        self.ensure_one()
        #self.mailing_counter = len(self.mailing_ids)
        selg.mailing_counter = self.env['mailing.trace'].search_count([
            ('model','=','res.partner'),
            ('res_id','=',self.id)
        ])
    mailing_counter = fields.Integer('Mailing Counter', compute='_get_mailing_counter')
    #mailing_ids = fields.One2many('mailing.trace', 'partner_id', 'Mailings')

    def call_contact_mailings(self):
        self.ensure_one()
        return {
		        'name':_("Mailings"),
                'type': 'ir.actions.act_window',
		        'view_type': 'form',
                'view_mode': 'tree,form',
		        'res_model': 'mailing.trace',
		        'target': 'current',
                'domain': [('model', '=', 'res.partner'),('res_id','=',self.id)]
                }

    """
    # A field to get the names of all the mailings the parter is associated to
    @api.depends('mailing_ids')
    def _get_mailing_titles(self):
        for s in self:
            titles = []
            for m in s.mailing_ids:
                titles.append(m.mass_mailing_id.subject)
            s.mailing_titles = ', '.join(titles)

    mailing_titles = fields.Char('Mailing titles',
                                    compute='_get_mailing_titles', store=True)
    """
    # Making mailings available in Contacts - END


# These changes are made in order to allow importing any value into the contacts.
# Whatever the state, it will always be saved.
class CountryState(models.Model):
    _inherit = 'res.country.state'

    country_id = fields.Many2one('res.country', required=False, index=True)
    name = fields.Char(index=True)
    code = fields.Char(required=False)

    @api.model
    def create(self, vals):
        if vals.get('name'):
            if not vals.get('country_id'):
                aux_country = '[unknown]'
                Country = self.env['res.country']
                country_id = Country.search([('name','=',aux_country)])
                if not country_id:
                    country_id = Country.create({
                                                'name': aux_country,
                                                'code': 'ZZ'
                                                })
                vals['country_id'] = country_id.id
            if not vals.get('code'):
                vals['code'] = uuid.uuid1()
        return super(CountryState, self).create(vals)
