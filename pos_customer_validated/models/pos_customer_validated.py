from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class PosCustomerValidated(models.Model):
    _inherit = 'res.partner'
    
    @api.model
    def create(self, vals):
        if 'vat' in vals:
            vat = vals['vat']
            customer = self.search([('vat', vat)])
            
            _logger.info(f'OBTENIENDO CUSTOMER DE LA BASE DE DATOS >>> { customer }')
            
        return super(PosCustomerValidated, self).create(vals)