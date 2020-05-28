# -*- coding: utf-8 -*-
import logging
import uuid

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


"""
Every model has a load() method. This could be used if we wanted to do changes
to imported data. However, our goal is to change the data before being imported, so,
we have to go to the mewthod that is executed for each line.
"""

# THIS SHOULD COME FROM base/models/ir_sequence.py rather then being redefined here
def _predict_nextval(self, seq_id):
    """Predict next value for PostgreSQL sequence without consuming it"""
    # Cannot use currval() as it requires prior call to nextval()
    query = """SELECT last_value,
                      (SELECT increment_by
                       FROM pg_sequences
                       WHERE sequencename = 'ir_sequence_%(seq_id)s'),
                      is_called
               FROM ir_sequence_%(seq_id)s"""
    if self.env.cr._cnx.server_version < 100000:
        query = "SELECT last_value, increment_by, is_called FROM ir_sequence_%(seq_id)s"
    self.env.cr.execute(query % {'seq_id': seq_id})
    (last_value, increment_by, is_called) = self.env.cr.fetchone()
    if is_called:
        return last_value + increment_by
    # sequence has just been RESTARTed to return last_value next time
    return last_value


DEBUG_MODE = True

class BaseModelExtend(models.AbstractModel):
    _name = 'basemodel.extend'
    _description = 'Base model extend'

    def _register_hook(self):

        def _sharevault_sharevault_check(self, data):
            if DEBUG_MODE:
                _logger.info("_sharevault_sharevault_check")
                _logger.info("ORIGINAL DATA: %s" % data)

            ShareVault = self.env['sharevault.sharevault']
            data_values = data['values']
            found_match = False

            if data_values.get('sharevault_id'):
                if DEBUG_MODE:
                    _logger.info("LOOKING FOR %s" % data_values['sharevault_id'])
                sharevault_exists = ShareVault.search([('sharevault_id','=ilike',data_values['sharevault_id'])], limit=1)
                if sharevault_exists:
                    if DEBUG_MODE:
                        _logger.info("SHAREVAULT FOUND")
                    for k in data_values.keys():
                        if not data_values[k]:
                            data_values[k] = eval('sharevault_exists.' + k)
                    found_match = sharevault_exists.id

            data['xml_id'] = ''
            if found_match:
                data_values['id'] = found_match

            if DEBUG_MODE:
                _logger.info("NEW DATA: %s" % data)
                if not found_match:
                    _logger.info("TO CREATE")
                else:
                    _logger.info("TO UPDATE (%s)" % data['values']['id'])
                _logger.info("---------------------------------------------------")

            return data


        # This method runs the rules defined by ShareVault and returns a dataset
        # that has been changed according to those rules
        def _sharevault_contact_check(self, data):
            if DEBUG_MODE:
                _logger.info("_sharevault_contact_check")
                _logger.info("ORIGINAL DATA: %s" % data)

            Partner = self.env['res.partner']
            data_values = data['values']
            found_match = False
            check_domain = False

            if data_values.get('email'):
                if DEBUG_MODE:
                    _logger.info("LOOKING FOR %s" % data_values['email'])
                # Is there an email like this one?
                email_exists = Partner.with_context(active_test=False).search([
                                            ('email','=ilike',data_values['email'])
                                            ], limit=1)
                if email_exists:
                    if DEBUG_MODE:
                        _logger.info("EMAIL FOUND")
                    # If there is an existing mail address, then, updates the
                    # record with the info on the file, except if the new info is blank
                    for k in data_values.keys():
                        # If the info in the file is blank, we use the one in the database
                        if not data_values[k]:
                            data_values[k] = eval('email_exists.' + k)
                    found_match = email_exists.id
                else:
                    check_domain = True
            else:
                check_domain = True

            if check_domain:
                if DEBUG_MODE:
                    _logger.info("LOOKING FOR NAME/DOMAIN %s/%s" % (data_values['name'],data_values['domain']))

                # If there is no email, it tries to match against name AND domain
                # then, updates the record with the info on the file, except if the new info is blank

                args_search_name_domain = [
                                            ('name','=ilike',data_values['name']),
                                            ('domain','=ilike',data_values['domain'])
                                            ]
                if data_values.get('is_company'):
                    args_search_name_domain.append(('is_company','=',data_values['is_company']))

                if DEBUG_MODE:
                    _logger.info("data_values: %s" % data_values)
                    _logger.info("args_search_name_domain: %s" % args_search_name_domain)

                name_domain_exists = Partner.with_context(active_test=False).search(args_search_name_domain)
                if name_domain_exists:
                    if DEBUG_MODE:
                        _logger.info("NAME+DOMAIN FOUND")
                    #if the info in the file is blank, it is replaced by the info in db
                    for k in data_values.keys():
                        if not data_values[k]:
                            data_values[k] = eval('name_domain_exists.' + k)
                    found_match = name_domain_exists.id

            if not found_match:
                if not data_values.get('email') and not data_values.get('is_company'):
                    if self._context.get('import_test_mode'):
                        # For testing purposes, we just create a fake sequence
                        sequence = uuid.uuid1()
                    else:
                        sequence = self.env['ir.sequence']\
                                        .next_by_code('res.partner.import')
                    sequence = str(sequence)

                    if not data_values.get('domain'):
                        data_values['email'] = sequence + '-unk@unkowndomain.com'
                    else:
                        data_values['email'] = sequence + '-unk@' + data_values['domain']

                    if DEBUG_MODE:
                        _logger.info("APPLYING NEW EMAIL %s" % data_values['email'])

                # Let's make sure the record is created
                data['xml_id'] = ''
            else:
                # We return an 'id' so that the system will take this as
                # an update. We also clean the xmlid
                data_values['id'] = found_match
                data['xml_id'] = ''

            if not data['values'].get('name'):
                data['values']['name'] = data['values']['email']

            if DEBUG_MODE:
                _logger.info("NEW DATA: %s" % data)
                if not found_match:
                    _logger.info("TO CREATE")
                else:
                    _logger.info("TO UPDATE (%s)" % data['values']['id'])
                _logger.info("---------------------------------------------------")

            return data

        models.BaseModel._sharevault_sharevault_check = _sharevault_sharevault_check
        models.BaseModel._sharevault_contact_check = _sharevault_contact_check

        return super(BaseModelExtend, self)._register_hook()


class BaseModelExtend(models.AbstractModel):
    _inherit = 'base'

    def _load_records(self, data_list, update=False):
        if DEBUG_MODE:
            _logger.info("_load_records SUPER")
        # We prepare the data according to SV's rules
        # This way, the rest of the code remains unchanged
        BaseObj = self.env['base']
        for data in data_list:
            if 'xml_id' in data and data.get('xml_id'):
                if 'sharevault' in data.get('xml_id').lower():
                    if DEBUG_MODE:
                        _logger.info("ShareVault import")
                    try:
                        data = BaseObj._sharevault_sharevault_check(data)
                    except Exception as e:
                        # _logger.error("ERROR: %s" % e)
                        pass

                if 'partner' in data.get('xml_id').lower():
                    if DEBUG_MODE:
                        _logger.info("Contact import")
                    try:
                        data = BaseObj._sharevault_contact_check(data)
                    except Exception as e:
                        _logger.error("ERROR: %s" % e)
                        pass
        return super(BaseModelExtend, self)._load_records(data_list, update=update)
