from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging, stdnum
_logger = logging.getLogger(__name__)

def verify_final_consumer(vat):
    return vat == '9' * 13

class PosCustomerValidated(models.Model):
    _inherit = 'res.partner'
    
    @api.model
    def create_from_ui(self, partner):
        _logger.info(f'SE OBTIENE CUSTOMER DEL FRONT >>> { partner }')
        if partner.get('vat') and partner['id'] == False:
            vat = partner['vat']
            longitud = len(vat)
            
            result = self._l10n_ec_vat_validation(vat)
            
            _logger.info(f'VALIDACION DE VAT >>> { result }')
            
            customer_vat = self.search([( 'vat', '=', vat )])
            
            
            
            customer_ruc = self.search([('vat', '=', vat)])
            
            if customer_vat or customer_ruc:
                raise ValidationError('El número de identificación ya existe.')
            
        return super(PosCustomerValidated, self).create_from_ui(partner)
    
    def _l10n_ec_vat_validation(self, vat):
        vat_validation = None
        ruc = stdnum.util.get_cc_module("ec", "ruc")
        ci = stdnum.util.get_cc_module("ec", "ci")
        self.l10n_ec_vat_validation = False
        final_consumer = verify_final_consumer(vat)
        _logger.info(f'OBTENIENDO FINAL CONSUMER >>> { final_consumer }')
        if not final_consumer:
            if not ci.is_valid(vat):
                vat_validation = f"The VAT { vat } seems to be invalid as the tenth digit doesn't comply with the validation algorithm (could be an old VAT number)"
            if not ruc.is_valid(vat):
                vat_validation = f"The VAT { vat } seems to be invalid as the tenth digit doesn't comply with the validation algorithm (SRI has stated that this validation is not required anymore for some VAT numbers)"
                
        return vat_validation