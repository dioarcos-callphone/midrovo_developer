from odoo import models, api
from odoo.exceptions import ValidationError
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class InvoiceDetails(models.AbstractModel):
    _name = 'report.account_due.report_account_due'
    _description = 'Reporte de Detalles de Facturas'
    
    @api.model
    def _get_report_values(self, docids, data=None):
        data_invoice_details = []
        court_date = data['court_date']
        client_id = data['client_id']
        journal_id = data['journal_id']
        comercial_id = data['comercial_id']
        
        _logger.info(f'MOSTRANDO DATA >>> { data }')
        
        domain = [
            ('move_id.invoice_date_due', '<=', court_date),
            ('amount_residual', '>', 0),
            ('partner_id', '=', client_id),
            ('move_id.move_type', 'in', ['out_invoice', 'out_refund']),
            ('move_id.payment_state', 'in', ['not_paid', 'partial'])
        ]
        
        if journal_id:
            domain.append(('journal_id', '=', journal_id))
        if comercial_id:
            domain.append(('move_id.invoice_user_id', '=', comercial_id))
        
        invoice_details = self.env['account.move.line'].search(domain)
        
        if invoice_details:
            _logger.info(f'MOSTRANDO INVOICE DETAILS >>> { invoice_details }')
            
            for detail in invoice_details:
                data_detail = {}
                
                date_formated = datetime.strftime(detail.move_id.invoice_date_due, "%d/%m/%Y")
                
                # añadimos los valores a los campos del diccionario
                data_detail['date_due'] = date_formated
                data_detail['numero'] = detail.move_name
                data_detail['diario_contable'] = detail.journal_id.name
                data_detail['comercial'] = detail.move_id.invoice_user_id.partner_id.name
                data_detail['cliente'] = detail.partner_id.name or ""
                data_detail['amount_residual'] = detail.amount_residual
  
                data_invoice_details.append(data_detail)
            
            return {
                'doc_ids': docids,
                'doc_model': 'report.account_due.report_account_due',
                'data': data,
                'options': data_invoice_details,
            }
        else:
            raise ValidationError("¡No se encontraron registros para los criterios dados!")
        