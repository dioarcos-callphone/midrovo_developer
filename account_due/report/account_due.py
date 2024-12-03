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
            ('payment_state', 'in', ['not_paid', 'partial'])
        ]
        
        domain_cogs = [
            ('product_id', '!=', False),
            ('display_type', '=', 'cogs'),
            ('date', '<=', court_date),
        ]
        
        # trae todas las lineas de factura para filtrar las que son de la cuenta 5
        details_account_five = self.env['account.move.line'].search(domain_cogs)
        
        if journal_id:
            domain.append(('journal_id', '=', journal_id))
        if comercial_id:
            domain.append(('move_id.invoice_user_id', '=', comercial_id))
        
        invoice_details = self.env['account.move.line'].search(domain)
        
        if invoice_details:
            _logger.info(f'MOSTRANDO INVOICE DETAILS >>> { invoice_details }')
            
            for invoice_detail in invoice_details:
                _logger.info(f'FACTURA #: { invoice_detail.move_name }')
                _logger.info(f'MONTO RESIDUAL: { invoice_detail.amount_residual }')
            
            # filtramos las lineas de factura cuyo codigo de cuenta comienza con 5
            details_account_five = details_account_five.filtered(
                lambda d : d.account_id.code.startswith('5')
            )
            
            # recorremos las lineas de factura de codigo 5 y traemos ciertos campos
            details_account_five = [ {
                'id': d.id,
                'date': d.date,
                'move_id': d.move_id.id,
                'journal_id': d.journal_id.id,
                'account_id': d.account_id.id,
                'product_id': d.product_id.id,
                'move_name': d.move_name,
                'debit': d.debit,
                'quantity': abs(d.quantity)
            } for d in details_account_five ]
            
            for detail in invoice_details:
                data_detail = {}
                debito = detail.debit
                
                for d_five in details_account_five:
                    # comparamos las lineas de factura de la cuenta 5 con las lineas de factura
                    # del asiento contable de facturas de cliente
                    if(
                        detail.date == d_five['date'] and
                        detail.move_id.id == d_five['move_id'] and
                        detail.product_id.id == d_five['product_id'] and
                        detail.quantity == d_five['quantity']                   
                    ):
                        debito = round(d_five['debit'], 2)
                
                data_detail['debito'] = debito

                descuento = round(0.00, 2)
                subtotal = detail.price_unit * detail.quantity
                
                if detail.discount:
                    descuento = round((subtotal * (detail.discount/100)),2)
                
                date_formated = datetime.strftime(detail.date, "%d/%m/%Y")
                
                # añadimos los valores a los campos del diccionario
                data_detail['fecha'] = date_formated
                data_detail['numero'] = detail.move_name
                data_detail['diario_contable'] = detail.journal_id.name
                data_detail['comercial'] = detail.move_id.invoice_user_id.partner_id.name
                data_detail['pos'] = detail.move_id.pos_order_ids.employee_id.name or ""
                data_detail['cliente'] = detail.partner_id.name or ""
                data_detail['producto'] = detail.product_id.name
                data_detail['cantidad'] = abs(detail.quantity)
                data_detail['precio'] = abs(detail.price_unit)
                data_detail['descuento'] = abs(descuento)
                data_detail['subtotal'] = abs(detail.price_subtotal)
                data_detail['costo'] = abs(round(detail.product_id.standard_price, 2))
  
                data_invoice_details.append(data_detail)
            
            return {
                'doc_ids': docids,
                'doc_model': 'report.account_due.report_account_due',
                'data': data,
                'options': data_invoice_details,
            }
        else:
            return {
                'doc_ids': docids,
                'doc_model': 'report.account_due.report_account_due',
                'data': data,
                'options': data_invoice_details,
            }
            # raise ValidationError("¡No se encontraron registros para los criterios dados!")
        