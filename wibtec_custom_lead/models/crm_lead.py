# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import ValidationError


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
