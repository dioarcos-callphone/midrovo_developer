from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class SriXmlDataExtend(models.Model):
    _inherit = 'sri.xml.data'
    _description = 'SRI XML Data Extend'
    
    @api.model
    def generate_info_tributaria(
        self,
        xml_id,
        node,
        document_type,
        environment,
        emission,
        company,
        printer_id,
        sequence,
        date_document
    ):
        
        result = super(SriXmlDataExtend, self).generate_info_tributaria(
            xml_id,
            node,
            document_type,
            environment,
            emission,
            company,
            printer_id,
            sequence,
            date_document
        )
        
        key_model = self.env['sri.keys']
        
        xml_data = self.browse(xml_id)
        
        if not xml_data.key_id:
            key_id = key_model.get_next_key(environment, emission)
            
            _logger.info(f'MOSTRANDO KEY ID 1 >>> { key_id }')

        else:
            key_id = xml_data.key_id.id
            
            _logger.info(f'MOSTRANDO KEY ID 2 >>> { key_id }')
            
        clave_acceso = xml_data.xml_key
        
        if not clave_acceso:
            clave_acceso = key_model.get_single_key(
                key_id,
                document_type,
                environment,
                printer_id,
                sequence,
                emission,
                xml_data.xml_type,
                date_document
            )
        
        _logger.info(f'CLAVE DE ACCESO >>> { clave_acceso }')
        
        return result