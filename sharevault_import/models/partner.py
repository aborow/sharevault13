# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import re

from odoo import api, fields, models
from odoo.osv.expression import get_unaccent_wrapper
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)

class Partner(models.Model):
    _inherit = 'res.partner'

    parent_id_domain = fields.Char(index=True, related="parent_id.domain")
    domain = fields.Char(index=True)
    email = fields.Char(index=True)
    is_company = fields.Boolean(index=True)

    @api.model
    def create(self, vals):
        self.check_uniqueness(vals)
        return super(Partner, self).create(vals)

    def write(self, vals):
        self.check_uniqueness(vals)
        return super(Partner, self).write(vals)



    # Constraint needs to be created in create() and write()
    def check_uniqueness(self, vals):
        _logger.info("XXXXX check_uniqueness XXXXX")
        _logger.info(vals)

        Partner = self.env['res.partner']
        if self.id:
            operation = 'write'
            if 'is_company' in vals:
                is_company = vals.get('is_company', '')
            else:
                is_company = self.is_company
            if 'name' in vals:
                name = vals.get('name', '')
            else:
                name = self.name
            if 'domain' in vals:
                domain = vals.get('domain', '')
            else:
                domain = self.domain
            if 'email' in vals:
                email = vals.get('email', '')
            else:
                email = self.email
            if 'parent_id' in vals:
                parent_id = vals.get('parent_id', False)
            else:
                parent_id = self.parent_id and self.parent_id.id or False
        else:
            operation = 'create'
            is_company = vals.get('is_company')
            name = vals.get('name', '')
            domain = vals.get('domain', '')
            email = vals.get('email', '')
            parent_id = vals.get('parent_id', False)

        _logger.info("Self (ID): %s / Operation: %s / Name: %s / Domain: %s / Email: %s / Parent ID: %s"\
                        % (self.id, operation, name, domain, email, parent_id))

        #1.  For a Company Type record - Name + Domain should always be unique
        #2.  For a contact type record - Name + related company (i.e. parent) + domain + email should always be unique

        args_search = [('id','!=',0)]
        fields_check = []
        if is_company == True:
            args_search = [
                            ('name','=ilike',name),
                            ('domain','=ilike',domain),
                            ('is_company','=',is_company)
                            ]
            fields_check = ['Name', 'Domain']
            if self.id:
                args_search.append(('id','!=',self.id))
        else:
            args_search = [
                            ('name','=ilike',name),
                            ('domain','=ilike',domain),
                            ('email','=ilike',email),
                            ('is_company','=',is_company),
                            ('parent_id','=',parent_id or False)
                            ]
            fields_check = ['Name', 'Domain', 'Email', 'Related Company']
            if self.id:
                args_search.append(('id','!=',self.id))

        if fields_check:
            _logger.info("args_search: %s" % args_search)
            find_dup = Partner.with_context(active_test=False).search(args_search)
            if find_dup:
                _logger.info("FIND_DUP: %s" % find_dup)
                raise ValidationError('There are, already partners with the same info: %s' % ' / '.join(fields_check))


    # A partner's name was not being properly searched when the contact was of the
    # individual type and still attached to a company. This happened because Odoo
    # searches against display_name but uses name (and this one does not include the
    # company's name)

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        self = self.with_user(name_get_uid or self.env.uid)
        # as the implementation is in SQL, we force the recompute of fields if necessary
        self.recompute(['display_name'])
        self.flush()
        if args is None:
            args = []
        order_by_rank = self.env.context.get('res_partner_search_mode')
        if (name or order_by_rank) and operator in ('=', 'ilike', '=ilike', 'like', '=like'):
            self.check_access_rights('read')
            where_query = self._where_calc(args)
            self._apply_ir_rules(where_query, 'read')
            from_clause, where_clause, where_clause_params = where_query.get_sql()
            from_str = from_clause if from_clause else 'res_partner'
            where_str = where_clause and (" WHERE %s AND " % where_clause) or ' WHERE '

            # search on the name of the contacts and of its company
            search_name = name
            if operator in ('ilike', 'like'):
                search_name = '%%%s%%' % name
            if operator in ('=ilike', '=like'):
                operator = operator[1:]

            unaccent = get_unaccent_wrapper(self.env.cr)
            fields = self._get_name_search_order_by_fields()

            # SV - let's make sure we get the display name for a record
            # that is a child of another
            # Sure... there probably is a better and more elegant way of doing this...
            mind_parent_query = False
            if 'import_file' in self._context:
                mind_parent_query = True

            if mind_parent_query:
                _logger.info("CASE 1")
                query = """SELECT res_partner.id
                             FROM {from_str}
		                           LEFT JOIN res_partner AS partner_company ON res_partner.parent_id=partner_company.id
                          {where} ({email} {operator} {percent}
                               OR {display_name} {operator2} {percent}
                               OR {reference} {operator} {percent}
                               OR {vat} {operator} {percent}
                               OR (
                                    res_partner.parent_id IS NOT NULL
                                    AND {display_name} ILIKE CONCAT({partner_company_name}, ', ', {percent})
                               ))

                         ORDER BY {fields} {display_name} {operator} {percent} desc,
                                  {display_name}
                        """.format(from_str=from_str,
                                   fields=fields,
                                   where=where_str,
                                   operator=operator,
                                   operator2='ILIKE',
                                   email=unaccent('res_partner.email'),
                                   display_name=unaccent('res_partner.display_name'),
                                   reference=unaccent('res_partner.ref'),
                                   percent=unaccent('%s'),
                                   vat=unaccent('res_partner.vat'),
                                   partner_company_name=unaccent('partner_company.name'),)
            else:
                _logger.info("CASE 2")
                query = """SELECT res_partner.id
                             FROM {from_str}
                          {where} ({email} {operator} {percent}
                               OR {display_name} {operator2} {percent}
                               OR {reference} {operator} {percent}
                               OR {vat} {operator} {percent}
                               )

                         ORDER BY {fields} {display_name} {operator} {percent} desc,
                                  {display_name}
                        """.format(from_str=from_str,
                                   fields=fields,
                                   where=where_str,
                                   operator=operator,
                                   operator2='ILIKE',
                                   email=unaccent('res_partner.email'),
                                   display_name=unaccent('res_partner.display_name'),
                                   reference=unaccent('res_partner.ref'),
                                   percent=unaccent('%s'),
                                   vat=unaccent('res_partner.vat'),)

            where_clause_params += [search_name]*3  # for email / display_name, reference
            where_clause_params += [re.sub('[^a-zA-Z0-9]+', '', search_name) or None]  # for vat

            if mind_parent_query:
                where_clause_params += [name]

            where_clause_params += [search_name]  # for order by
            if limit:
                query += ' limit %s'
                where_clause_params.append(limit)

            self.env.cr.execute(query, where_clause_params)

            # SV - Check the query that was executed
            _logger.info(str(self.env.cr.query).replace('\\n', ' ').replace('\\t', ' ').replace('\\', ""))
            _logger.info("ARGS: %s" % args)
            _logger.info("mind_parent_query: %s" % mind_parent_query)

            partner_ids = [row[0] for row in self.env.cr.fetchall()]

            if partner_ids:

                # SV - if there are several records, we just choose one.
                # This way we avoid conflicts.
                if mind_parent_query:
                    try:
                        partner_ids = partner_ids[0]
                    except Exception as e:
                        _logger.error(e)
                        pass

                return models.lazy_name_get(self.browse(partner_ids))
            else:
                return []
        return super(Partner, self)._name_search(name, args, operator=operator, limit=limit, name_get_uid=name_get_uid)
