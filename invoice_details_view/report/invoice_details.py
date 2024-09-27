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
        cashier = data['cashier']
        
        domain = [
            ('product_id', '!=', False),
            ('date', '>=', fecha_inicio),
            ('date', '<=', fecha_fin),
        ]
        
        if diario:
            domain.append(('journal_id', 'in', diario))
        if comercial:
            domain.append(('move_id.invoice_user_id', 'in', comercial))
        if cashier:
            domain.append(('move_id.pos_order_ids.employee_id', 'in', cashier))
        
        invoice_details = self.env['account.move.line'].search(domain)
        
        if invoice_details:           
            for detail in invoice_details:
                descuento = round(0.00, 2)
                subtotal = detail.price_unit * detail.quantity
                if detail.discount:
                    descuento = round((subtotal * (detail.discount/100)),2)
                
                total_costo = round((detail.product_id.standard_price * detail.quantity), 2)
                rentabilidad = detail.price_subtotal - total_costo
                
                data_detail = {
                    "numero": detail.move_name,
                    "comercial": detail.move_id.invoice_user_id.partner_id.name,
                    "pos": detail.move_id.pos_order_ids.employee_id.name,
                    "producto": detail.product_id.name,
                    "cantidad": detail.quantity,
                    "precio": detail.price_unit,
                    "descuento": descuento,
                    "subtotal": detail.price_subtotal,
                    "costo": round(detail.product_id.standard_price, 2),
                    "total_costo": total_costo,
                    "rentabilidad": round(rentabilidad, 2)
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