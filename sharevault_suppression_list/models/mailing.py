# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models
from odoo.exceptions import Warning,ValidationError

_logger = logging.getLogger(__name__)

# No edit will be allowed to make things easier
# If someone want to change the domain, he shoud delete it and create a new one
class MailSuppressionList(models.Model):
    _name = 'mail.suppression_list'
    _description = 'Domain Supression List for Emailing'

    name = fields.Char('Domain')
    use_in_webform = fields.Boolean('Use in webforms', default=True)
    use_in_mailing = fields.Boolean('Use in mailing', default=True)

    contact_ids = fields.One2many(
                                'mail.blacklist',
                                'suppression_list_id',
                                string='Blacklisted Contacts'
                                )
    def _get_contact_count(self):
        self.contact_count = len(self.contact_ids)

    contact_count = fields.Integer('Contact count',
                                    compute='_get_contact_count',
                                    help='Blacklisted contacts')

    @api.model
    def create(self, vals):
        new_record = super(MailSuppressionList, self).create(vals)
        if new_record:
            # Go through all existing contacts
            # add, go through all the contacts with an email like "domain" and blacklist them
            #Also set the opt_out that sharevault defines in res.partner - really ???!!!

            txtSQL = """
                        SELECT	email
                        FROM	mailing_contact
                        WHERE	email LIKE '%%@%s'
                        AND		email NOT IN (SELECT email FROM mail_blacklist)""" % vals['name']
            self._cr.execute(txtSQL)
            res = self._cr.fetchall()
            for r in res:
                self.env['mail.blacklist'].create({
                                                'email': r[0],
                                                'suppression_list_id': new_record.id
                                                })
        return new_record


    def unlink(self):
        for s in self:
            if s.contact_count:
                raise Warning(
                            """Removing a domain from the suppression list WILL NOT remove existing contacts from the blacklist.\n
There are currently %s contacts from this domain on the blacklist.\n
Please review and update those directly on the blacklist.\n
This suppression list entry was originally created on %s by %s.\n""" % (
                                                                        s.contact_count,
                                                                        s.create_date.replace(microsecond=0),
                                                                        s.create_uid.name
                                                                        )
                            )
        return super(MailSuppressionList, self).unlink()


class MailBlacklist(models.Model):
    _inherit = 'mail.blacklist'

    suppression_list_id = fields.Many2one('mail.suppression_list', 'Suppression List')
