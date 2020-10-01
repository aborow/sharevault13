
from odoo import api, models


class WibtecRibbonBackend(models.AbstractModel):

    _name = 'wibtec.ribbon.backend'
    _description = 'Wibtec Ribbon Backend'

    @api.model
    def _prepare_ribbon_format_vals(self):
        return {
            'db_name': self.env.cr.dbname,
        }

    @api.model
    def _prepare_ribbon_name(self):
        name_tmpl = self.env['ir.config_parameter'].sudo().get_param(
            'wb.ribbon.name')
        vals = self._prepare_ribbon_format_vals()
        return name_tmpl and name_tmpl.format(**vals) or name_tmpl

    @api.model
    def get_environment_ribbon(self):
        """
        This method returns the ribbon data from ir config parameters
        :return: dictionary
        """
        ir_config_model = self.env['ir.config_parameter']
        name = self._prepare_ribbon_name()
        return {
            'name': name,
            'color': ir_config_model.sudo().get_param('wb.ribbon.color'),
            'background_color': ir_config_model.sudo().get_param(
                'wb.ribbon.background.color'),
        }