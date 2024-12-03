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
        
        domain = [
            ('move_id.invoice_date_due', '<=', court_date),
            ('amount_residual', '>', 0),
            ('partner_id', '=', client_id),
            ('move_id.move_type', '=', 'out_invoice'),
            ('move_id.payment_state', 'in', ['not_paid', 'partial']),
            ('account_id.account_type', '=', 'asset_receivable'),
        ]
        
        if journal_id:
            domain.append(('journal_id', '=', journal_id))
        if comercial_id:
            domain.append(('move_id.invoice_user_id', '=', comercial_id))
        
        invoice_details = self.env['account.move.line'].search(domain)
        
        if invoice_details:            
            for detail in invoice_details:
                data_detail = {}
                
                date_formated = datetime.strftime(detail.move_id.invoice_date_due, "%d/%m/%Y")
                
                # añadimos los valores a los campos del diccionario
                data_detail['date_due'] = date_formated
                data_detail['invoice'] = detail.move_name
                data_detail['journal'] = detail.journal_id.name
                data_detail['comercial'] = detail.move_id.invoice_user_id.partner_id.name
                data_detail['client'] = detail.partner_id.name or ""
                data_detail['amount_residual'] = detail.amount_residual
                data_detail['account'] = detail.account_id.code
                data_detail['actual'] = False
                data_detail['1 - 30'] = False
                data_detail['31 - 60'] = False
                data_detail['61 - 90'] = False
                data_detail['91 - 120'] = False
                data_detail['antiguo'] = False
                
                
                fecha_vencida = detail.move_id.invoice_date_due
                fecha_actual = datetime.now()
                
                dias_transcurridos = (fecha_actual.date() - fecha_vencida).days
                
                # Determinar el rango
                if dias_transcurridos == 0:
                    data_detail['actual'] = data_detail['amount_residual']
                elif dias_transcurridos <= 30 and dias_transcurridos > 0:
                    data_detail['1 - 30'] = data_detail['amount_residual']
                elif dias_transcurridos <= 60:
                    data_detail['31 - 60'] = data_detail['amount_residual']
                elif dias_transcurridos <= 90:
                    data_detail['61 - 90'] = data_detail['amount_residual']
                elif dias_transcurridos <= 120:
                    data_detail['91 - 120'] = data_detail['amount_residual']
                else:
                    data_detail['antiguo'] = data_detail['amount_residual']
  
                data_invoice_details.append(data_detail)
                
            # _logger.info(f'MOSTRANDO RESULTADOS >>> { data_invoice_details }')
            
            return {
                'doc_ids': docids,
                'doc_model': 'report.account_due.report_account_due',
                'data': data,
                'options': data_invoice_details,
            }
        else:
            raise ValidationError("¡No se encontraron registros para los criterios dados!")
        