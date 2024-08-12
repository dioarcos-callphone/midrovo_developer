# -*- coding: utf-8 -*-

from odoo import fields, models, api 



class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    invoice_number_fact = fields.Boolean()

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('res.config.settings.invoice_number_fact', int(self.invoice_number_fact))

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        
        res['invoice_number_fact'] = int(
            get_param('res.config.settings.invoice_number_fact'))
        return res
