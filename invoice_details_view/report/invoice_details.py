from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

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
        is_cost_or_debit = data['is_cost_or_debit']
        
        domain = [
            ('product_id', '!=', False),
            ('display_type', '=', 'product'),
            ('date', '>=', fecha_inicio),
            ('date', '<=', fecha_fin),
            ('move_id.move_type', 'in', ['out_invoice', 'out_refund']),
        ]
        
        domain_cogs = [
            ('product_id', '!=', False),
            ('display_type', '=', 'cogs'),
            ('date', '>=', fecha_inicio),
            ('date', '<=', fecha_fin),
        ]
        
        # trae todas las lineas de factura para filtrar las que son de la cuenta 5
        details_account_five = self.env['account.move.line'].search(domain_cogs)
        
        if diario:
            domain.append(('journal_id', 'in', diario))
        if comercial:
            domain.append(('move_id.invoice_user_id', 'in', comercial))
        if cashier:
            domain.append(('move_id.pos_order_ids.employee_id', 'in', cashier))
        
        invoice_details = self.env['account.move.line'].search(domain)
        
        if invoice_details:
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
                
                if is_cost_or_debit == 'master':
                    total_costo = round((detail.product_id.standard_price * detail.quantity), 2)
                    
                if is_cost_or_debit == 'movement':
                    total_costo = round(data_detail['debito'], 2)
                    
                rentabilidad = detail.price_subtotal - total_costo
                
                date_formated = datetime.strftime(detail.date, "%d/%m/%Y")
                
                # añadimos los valores a los campos del diccionario
                data_detail['fecha'] = date_formated
                data_detail['numero'] = detail.move_name
                data_detail['diario_contable'] = detail.journal_id.name
                data_detail['comercial'] = detail.move_id.invoice_user_id.partner_id.name
                data_detail['pos'] = detail.move_id.pos_order_ids.employee_id.name or ""
                data_detail['cliente'] = detail.partner_id.name or ""
                data_detail['producto'] = detail.product_id.name
                data_detail['cantidad'] = detail.quantity
                data_detail['precio'] = detail.price_unit
                data_detail['descuento'] = descuento
                data_detail['subtotal'] = detail.price_subtotal
                data_detail['costo'] = round(detail.product_id.standard_price, 2)
                data_detail['total_costo'] = total_costo
                data_detail['rentabilidad'] = round(rentabilidad, 2)
                
                if detail.move_id.move_type == 'out_invoice':
                    data_detail['tipo'] = 'Factura'
                    
                elif detail.move_id.move_type == 'out_refund':
                    data_detail['tipo'] = 'Nota de crédito'
                    data_detail['rentabilidad'] = - data_detail['rentabilidad']
                    data_detail['total_costo'] = - data_detail['total_costo']
                    data_detail['costo'] = - data_detail['costo']
                    data_detail['cantidad'] = - data_detail['cantidad']
                    data_detail['precio'] = - data_detail['precio']
                    data_detail['descuento'] = - data_detail['descuento']
                    data_detail['subtotal'] = - data_detail['subtotal']
                    
                methods = self.env['pos.payment.method'].search_read([], ['name'])
                pos_order = detail.move_id.pos_order_ids
                
                for method in methods:
                    data_detail[method['name']] = 0
                    if pos_order:
                        for payment in pos_order.payment_ids:
                            if method['name'] == payment.payment_method_id.name:
                                data_detail[method['name']] = payment.amount
                    else:
                        journal_name = detail.move_id.invoice_payments_widget['journal_name']
                        amount = detail.move_id.invoice_payments_widget['amount']
                        if method['name'] == journal_name:
                            data_detail[method['name']] = amount

                    
                data_invoice_details.append(data_detail)
            
            return {
                'doc_ids': docids,
                'doc_model': 'report.invoice_details_view.report_invoice_details',
                'data': data,
                'options': data_invoice_details,
                'is_cost_or_debit': is_cost_or_debit
            }
        else:
            raise ValidationError("¡No se encontraron registros para los criterios dados!")