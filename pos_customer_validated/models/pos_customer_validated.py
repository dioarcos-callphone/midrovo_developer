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
        if partner.get('vat') and partner['id'] == False:
            vat = partner['vat']
            longitud = len(vat)
            
            if(longitud > 13 or longitud < 10):
                raise ValidationError('El número de identificación no es válido.')
            
            if(not self._l10n_ec_vat_validation(vat)):
                raise ValidationError(f'El número de identificación { vat } no existe.')
            
            cedula = vat if len(vat) == 10 else vat[:-3]
            ruc = vat if len(vat) == 13 else f'{ vat }001'
            
            _logger.info(f'CEDULA >> { cedula } || RUC >> { ruc }')
            
            customer_vat = self.search([( 'vat', '=', cedula )])
            customer_ruc = self.search([('vat', '=', ruc)])
            
            if customer_vat or customer_ruc:
                raise ValidationError(f'El número de identificación ya se encuentra registrado.')
            
        return super(PosCustomerValidated, self).create_from_ui(partner)
    
    def _l10n_ec_vat_validation(self, vat):
        vat_validation = False
        ruc = stdnum.util.get_cc_module("ec", "ruc")
        ci = stdnum.util.get_cc_module("ec", "ci")
        self.l10n_ec_vat_validation = False
        final_consumer = verify_final_consumer(vat)
        if not final_consumer:
            if ci.is_valid(vat) and len(vat) == 10:
                vat_validation = True
                
            elif ruc.is_valid(vat) and len(vat) == 13:
                vat_validation = True
                
        return vat_validation