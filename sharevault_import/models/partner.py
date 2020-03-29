# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import re

from odoo import api, fields, models
from odoo.osv.expression import get_unaccent_wrapper

_logger = logging.getLogger(__name__)

class Partner(models.Model):
    _inherit = 'res.partner'


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

            # ShareVault - let's make sure we get the display name for a record
            # that is a child of another
            # Sure... there probably is a better and more elegant way of doing this...

            mind_parent_query = False
            if 'XXXimport_file' in self._context:
                mind_parent_query = True

            if mind_parent_query:
                query = """SELECT res_partner.id
                             FROM {from_str}
		                           LEFT JOIN res_partner AS partner_company ON res_partner.parent_id=partner_company.id
                          {where} ({email} {operator} {percent}
                               OR {display_name} {operator} {percent}
                               OR {reference} {operator} {percent}
                               OR {vat} {operator} {percent}
                               OR (
                                    res_partner.parent_id IS NOT NULL
                                    AND {display_name} LIKE CONCAT(partner_company.name, ', ', {percent})
                               ))

                               -- don't panic, trust postgres bitmap
                         ORDER BY {fields} {display_name} {operator} {percent} desc,
                                  {display_name}
                        """.format(from_str=from_str,
                                   fields=fields,
                                   where=where_str,
                                   operator=operator,
                                   email=unaccent('res_partner.email'),
                                   display_name=unaccent('res_partner.display_name'),
                                   reference=unaccent('res_partner.ref'),
                                   percent=unaccent('%s'),
                                   vat=unaccent('res_partner.vat'),)
            else:
                query = """SELECT res_partner.id
                             FROM {from_str}
                          {where} ({email} {operator} {percent}
                               OR {display_name} {operator} {percent}
                               OR {reference} {operator} {percent}
                               OR {vat} {operator} {percent}
                               )

                               -- don't panic, trust postgres bitmap
                         ORDER BY {fields} {display_name} {operator} {percent} desc,
                                  {display_name}
                        """.format(from_str=from_str,
                                   fields=fields,
                                   where=where_str,
                                   operator=operator,
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

            # Check the query that was executed
            #_logger.info(self.env.cr.query)

            partner_ids = [row[0] for row in self.env.cr.fetchall()]

            if partner_ids:
                return models.lazy_name_get(self.browse(partner_ids))
            else:
                return []
        return super(Partner, self)._name_search(name, args, operator=operator, limit=limit, name_get_uid=name_get_uid)
