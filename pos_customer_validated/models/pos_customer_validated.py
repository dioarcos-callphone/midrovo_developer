from odoo import models, api
from odoo.exceptions import ValidationError
import logging, re
_logger = logging.getLogger(__name__)

identifiacion_regex = r"^(1|2|3|4|5|6|7|8|9)[0-9]{9}$"

class PosCustomerValidated(models.Model):
    _inherit = 'res.partner'
    
    @api.model
    def create_from_ui(self, partner):
        _logger.info(f'SE OBTIENE CUSTOMER DEL FRONT >>> { partner }')
        if partner.get('vat') and partner['id'] == False:
            vat = partner['vat']
            longitud = len(vat)
            
            result = self.validar_identificacion(vat)
            
            _logger.info(f'VALIDACION DE VAT >>> { result }')
            
            customer_vat = self.search([( 'vat', '=', vat )])
            
            
            
            customer_ruc = self.search([('vat', '=', vat)])
            
            if customer_vat or customer_ruc:
                raise ValidationError('El número de identificación ya existe.')
            
        return super(PosCustomerValidated, self).create_from_ui(partner)
    
    def validar_identificacion(self, identificacion):
        return re.match(identifiacion_regex, identificacion) is not None