from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class InvoiceDetails(models.AbstractModel):
    _name = 'report.invoice_details_view.report_invoice_details'
    _description = 'Reporte de Detalles de Facturas'
    
    @api.model
    def _get_report_values(self, docids, data=None):
        fecha_inicio = data['fecha_inicio']
        fecha_fin = data['fecha_fin']
        diario = data['diario']
        comercial = data['comercial']
        
        invoice_details = self.env['account.move.line'].search([
            ('date', '>=', fecha_inicio),
            ('date', '<=', fecha_fin),
            ('journal_id', 'in', diario),
            # ('comercial', 'in', comercial),    
        ])
        
        if invoice_details:
            _logger.info(f'MOSTRANDO INVOICE DETAILS >>> { invoice_details }')
            
            return {
                'doc_ids': docids,
                'doc_model': 'report.invoice_details_view.report_invoice_details',
                'data': data,
                'options': invoice_details,
            }
        else:
            raise ValidationError("No records found for the given criteria!")