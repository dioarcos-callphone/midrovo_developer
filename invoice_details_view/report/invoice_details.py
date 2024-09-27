from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class InvoiceDetails(models.AbstractModel):
    _name = 'report.invoice_details_view.report_invoice_details'
    _description = 'Reporte de Detalles de Facturas'
    
    @api.model
    def _get_report_values(self, docids, data=None):
        data_invoice_details = []
        fecha_inicio = data['fecha_inicio']
        fecha_fin = data['fecha_fin']
        diario = data['diario']
        comercial = data['comercial']
        
        domain = [
            ('product_id', '!=', False),
            ('date', '>=', fecha_inicio),
            ('date', '<=', fecha_fin),
        ]
        
        if diario:
            domain.append(('journal_id', 'in', diario))
        if comercial:
            domain.append(('move_id.invoice_user_id', 'in', comercial))
        
        invoice_details = self.env['account.move.line'].search(domain)
        
        if invoice_details:            
            for detail in invoice_details:
                descuento = 0.00
                subtotal = detail.price_unit * detail.quantity
                if detail.discount:
                    descuento = subtotal - (subtotal * (detail.discount/100))
                
                data_detail = {
                    "numero": detail.move_name,
                    "comercial": detail.move_id.invoice_user_id.partner_id.name,
                    "producto": detail.product_id.name,
                    "cantidad": detail.quantity,
                    "precio": detail.price_unit,
                    "descuento": descuento,
                    "subtotal": subtotal,
                    "costo": round(detail.product_id.standard_price, 2),
                }
                
                data_invoice_details.append(data_detail)
            
            return {
                'doc_ids': docids,
                'doc_model': 'report.invoice_details_view.report_invoice_details',
                'data': data,
                'options': data_invoice_details,
            }
        else:
            raise ValidationError("¡No se encontraron registros para los criterios dados!")