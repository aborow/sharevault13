# -*- coding: utf-8 -*-
import logging
import uuid

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


"""
Every model has a load() method. This could be used if we wanted to do changes
to imported data. However, our goal is to change the data before being imported, so,
we have to go to the mewthod that is executed for each line.

[ RULES ]
----------------------------------------------------------------------------
If there is an existing mail address, then, updates the record with the info
    on the file, except if the new info is blank

If there is no email, it tries to match against name AND domain
    and the behaviour is the same


If no match is found, we create a new record
    ... and ...

    if email is blank:
        if domain is blank
        email = sequence of [sequence]-unk@unkowndomain.com

        if domain is populated
        email = sequence of [sequence]-unk@[domain.com]
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

    def _register_hook(self):

        # This method runs the rules defined by ShareVault and returns a dataset
        # that has been changed according to those rules
        def _sharevault_check(self, data):
            if DEBUG_MODE:
                _logger.info("_sharevault_check")
                _logger.info("SV prepare")
                _logger.info("ORIGINAL DATA: %s" % data)
                _logger.info(self.env.context)


            Partner = self.env['res.partner']
            data_values = data['values']
            found_match = False
            check_domain = False

            if data_values.get('email'):
                if DEBUG_MODE:
                    _logger.info("LOOKING FOR %s" % data_values['email'])
                # Is there an email like this one?
                email_exists = Partner.search([('email','=ilike',data_values['email'])], limit=1)
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

            if check_domain:
                if DEBUG_MODE:
                    _logger.info("LOOKING FOR NAME/DOMAIN %s/%s" % (data_values['name'],data_values['domain']))

                # If there is no email, it tries to match against name AND domain
                # then, updates the record with the info on the file, except if the new info is blank
                name_domain_exists = Partner.search([
                                                    ('name','=ilike',data_values['name']),
                                                    ('domain','=ilike',data_values['domain'])
                                                    ])
                if name_domain_exists:
                    if DEBUG_MODE:
                        _logger.info("NAME+DOMAIN FOUND")
                    #if the info in the file is blank, it is replaced by the info in db
                    for k in data_values.keys():
                        if not data_values[k]:
                            data_values[k] = eval('name_domain_exists.' + k)
                    found_match = name_domain_exists.id

            if not found_match:
                if not data_values.get('email'):
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

        """
        # TEST - START
        # This is just the original method, so that we can log values
        def _sharevault_load_records(self, data_list, update=False):

            _logger.info("AAAAA _sharevault_load_records AAAAA")

            original_self = self.browse()
            # records created during installation should not display messages
            self = self.with_context(install_mode=True)
            imd = self.env['ir.model.data'].sudo()

            # The algorithm below partitions 'data_list' into three sets: the ones
            # to create, the ones to update, and the others. For each set, we assign
            # data['record'] for each data. All those records are then retrieved for
            # the result.

            # determine existing xml_ids
            xml_ids = [data['xml_id'] for data in data_list if data.get('xml_id')]
            existing = {
                ("%s.%s" % row[1:3]): row
                for row in imd._lookup_xmlids(xml_ids, self)
            }

            # ShareVault - START **********************************************
            # We prepare the data according to SV's rules
            # This way, the rest of the code remains unchanged
            #for data in data_list:
            #    if 'res_partner' in data.get('xml_id'):
            #        data = self._sharevault_check(data)
            # ShareVault - END ************************************************

            # determine which records to create and update
            to_create = []                  # list of data
            to_update = []                  # list of data

            #for each line...
            for data in data_list:
                xml_id = data.get('xml_id')
                if not xml_id:
                    vals = data['values']
                    if vals.get('id'):
                        data['record'] = self.browse(vals['id'])
                        to_update.append(data)
                    elif not update:
                        to_create.append(data)
                    continue

                row = existing.get(xml_id)
                # If the xmlid does not exist in the database
                if not row:
                    # Record will be created
                    to_create.append(data)
                    # Move on to the next record
                    continue

                # The record exists, let's get some values
                d_id, d_module, d_name, d_model, d_res_id, d_noupdate, r_id = row
                record = self.browse(d_res_id)
                if update and d_noupdate:
                    data['record'] = record
                elif r_id:
                    data['record'] = record
                    to_update.append(data)
                else:
                    imd.browse(d_id).unlink()
                    to_create.append(data)

            # update existing records
            for data in to_update:
                data['record']._load_records_write(data['values'])

            # determine existing parents for new records
            for parent_model, parent_field in self._inherits.items():
                suffix = '_' + parent_model.replace('.', '_')
                xml_ids_vals = {
                    (data['xml_id'] + suffix): data['values']
                    for data in to_create
                    if data.get('xml_id')
                }
                for row in imd._lookup_xmlids(xml_ids_vals, self.env[parent_model]):
                    d_id, d_module, d_name, d_model, d_res_id, d_noupdate, r_id = row
                    if r_id:
                        xml_id = '%s.%s' % (d_module, d_name)
                        xml_ids_vals[xml_id][parent_field] = r_id
                    else:
                        imd.browse(d_id).unlink()

            # check for records to create with an XMLID from another module
            module = self.env.context.get('install_module')
            if module:
                prefix = module + "."
                for data in to_create:
                    if data.get('xml_id') and not data['xml_id'].startswith(prefix):
                        _logger.warning("Creating record %s in module %s.", data['xml_id'], module)

            # create records
            records = self._load_records_create([data['values'] for data in to_create])
            for data, record in zip(to_create, records):
                data['record'] = record

            # create or update XMLIDs
            if to_create or to_update:
                imd_data_list = [data for data in data_list if data.get('xml_id')]
                imd._update_xmlids(imd_data_list, update)

            return original_self.concat(*(data['record'] for data in data_list))

        models.BaseModel._load_records = _sharevault_load_records
        # TEST - END
        """


        models.BaseModel._sharevault_check = _sharevault_check

        return super(BaseModelExtend, self)._register_hook()


class BaseModelExtend(models.AbstractModel):
    _inherit = 'base'

    def _load_records(self, data_list, update=False):
        if DEBUG_MODE:
            _logger.info("_load_records SUPER")
        # We prepare the data according to SV's rules
        # This way, the rest of the code remains unchanged
        for data in data_list:
            if 'partner' in data.get('xml_id'):
                try:
                    data = self.env['base']._sharevault_check(data)
                except Exception as e:
                    _logger.error("ERROR: %s" % e)
                    pass
        return super(BaseModelExtend, self)._load_records(data_list, update=update)
