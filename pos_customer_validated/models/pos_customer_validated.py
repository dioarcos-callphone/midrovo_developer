from odoo import models, api
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class PosCustomerValidated(models.Model):
    _inherit = 'res.partner'
    
    @api.model
    def create_from_ui(self, partner):
        _logger.info(f'SE OBTIENE CUSTOMER DEL FRONT >>> { partner }')
        if partner.get('vat'):
            vat = partner['vat']
            
            customer = self.search([( 'vat', '=', vat )])
            
            if customer:
                raise ValidationError('Este ruc ya existe')
            
        return super(PosCustomerValidated, self).create_from_ui(partner)