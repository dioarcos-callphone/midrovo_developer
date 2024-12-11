from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class SriKeyExtend(models.Model):
    _inherit = "sri.keys"
    
    @api.model
    def get_single_key(
        self,
        key_id,
        type_voucher,
        environment,
        printer_point_id,
        sequence,
        emission,
        xml_type='individual',
        date_document=None
    ):
        result = super(SriKeyExtend, self).get_single_key(
            key_id,
            type_voucher,
            environment,
            printer_point_id,
            sequence,
            emission,
            xml_type,
            date_document
        )
        
        # _logger.info(f'MOSTRANDO TYPE VOUCHER >>>> { type_voucher }')
        
        return result