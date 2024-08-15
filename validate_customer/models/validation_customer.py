from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ValidationCustomer(models.Model):
    _inherit = 'res.partner'
    
    @api.constrains('vat')
    def _validate_vat_ruc(self):
        identificacion = self.vat
        id_existente = self.search([('vat', '=', identificacion)])
        if id_existente:
            raise ValidationError('Usuario ya existe')