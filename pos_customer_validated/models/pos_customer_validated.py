from odoo import models, api
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class PosCustomerValidated(models.Model):
    _inherit = 'res.partner'
    
    @api.model
    def create_from_ui(self, partner):
        _logger.info(f'SE OBTIENE CUSTOMER DEL FRONT >>> { partner }')
        if partner.get('vat') and partner['id'] == False:
            
            _logger.info(f'LONGITUD DEL VAT >>> { len(partner['vat']) }')
            
            vat = partner['vat']
            
            customer_vat = self.search([( 'vat', '=', vat )])
            
            
            
            customer_ruc = self.search([('vat', '=', vat)])
            
            if customer_vat or customer_ruc:
                raise ValidationError('El número de identificación ya existe.')
            
        return super(PosCustomerValidated, self).create_from_ui(partner)