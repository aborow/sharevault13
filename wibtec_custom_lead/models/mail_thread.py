# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    def _message_auto_subscribe_notify(self, partner_ids, template):
        """ Notify new followers, using a template to render the content of the
        notification message. Notifications pushed are done using the standard
        notification mechanism in mail.thread. It is either inbox either email
        depending on the partner state: no user (email, customer), share user
        (email, customer) or classic user (notification_type)

        :param partner_ids: IDs of partner to notify;
        :param template: XML ID of template used for the notification;
        """
        if not self or self.env.context.get('mail_auto_subscribe_no_notify'):
            return
        if not self.env.registry.ready:  # Don't send notification during install
            return

        view = self.env['ir.ui.view'].browse(self.env['ir.model.data'].xmlid_to_res_id(template))

        for record in self:
            if record._name == 'crm.lead':
                model_description = self.env['ir.model']._get(record._name).display_name
                values = {
                    'object': record,
                    'model_description': model_description,
                }
                partners = self.get_partner_ids(partner_ids, record)
                assignation_msg = view.render(values, engine='ir.qweb', minimal_qcontext=True)
                assignation_msg = self.env['mail.thread']._replace_local_links(assignation_msg)
                record.message_notify(
                    subject=_('New LEAD created for %s') % record.display_name,
                    body=assignation_msg,
                    partner_ids=partners,
                    record_name=record.display_name,
                    email_layout_xmlid='mail.mail_notification_light',
                    model_description=model_description,
                )

    def get_partner_ids(self, partner_ids, record):
        if record.team_id:
            if record.team_id.team_user_ids:
                partners = [team_user.user_id.partner_id.id for team_user in record.team_id.team_user_ids]
                partners.append(partner_ids[0])
                team_partners = list(set(partners))
                return team_partners
            else:
                return partner_ids
