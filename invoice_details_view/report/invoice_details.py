from odoo import models, api
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
        is_cost_or_debit = data.get('is_cost_or_debit', None)
        is_resumen = data.get('is_resumen', None)
        
        if is_resumen == 'r':
            data_invoices = self.get_report_facturas(fecha_inicio, fecha_fin, comercial, cashier, diario)
            return {
                'doc_ids': docids,
                'doc_model': 'report.invoice_details_view.report_invoice_details',
                'data': data,
                'options': data_invoices,
                'is_resumen': is_resumen
            }
        
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
                data_detail['cantidad'] = abs(detail.quantity)
                data_detail['precio'] = abs(detail.price_unit)
                data_detail['descuento'] = abs(descuento)
                data_detail['subtotal'] = abs(detail.price_subtotal)
                data_detail['costo'] = abs(round(detail.product_id.standard_price, 2))
                data_detail['total_costo'] = abs(total_costo)
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
  
                metodos = []
                
                payment_widget = detail.move_id.invoice_payments_widget
                
                if payment_widget:
                    contents = payment_widget['content']
                    
                    for content in contents:
                        pos_payment_name = content.get('pos_payment_name', None)
                        
                        if not pos_payment_name:
                            journal_name = content['journal_name']
                            
                            if journal_name == 'Point of Sale':
                                pos_order = detail.move_id.pos_order_ids
                                if pos_order:
                                    for payment in pos_order.payment_ids:
                                        metodos.append(payment.payment_method_id.name)
                            else:              
                                metodos.append(journal_name)
                                
                        else:
                            pos_order = detail.move_id.pos_order_ids
                    
                            # Se evalua el metodo de pago (cuenta por cobrar) no contiene journal_type
                            if pos_order:
                                for payment in pos_order.payment_ids:
                                    if not payment.payment_method_id.journal_id:
                                        metodos.append(payment.payment_method_id.name)
                            
                            metodos.append(pos_payment_name)
                
                else:
                    pos_order = detail.move_id.pos_order_ids
                    
                    # Se evalua el metodo de pago (cuenta por cobrar) no contiene journal_type
                    if pos_order:
                        for payment in pos_order.payment_ids:
                            metodos.append(payment.payment_method_id.name)
                
                metodos_set = set(metodos)
                metodos_list = list(metodos_set)
                                    
                data_detail['metodos'] = metodos_list
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
        
    
    def get_report_facturas(self, fecha_inicio, fecha_fin, comercial, cashier, diario):        
        data_invoice_details = []
        domain = [
            ('date', '>=', fecha_inicio),
            ('date', '<=', fecha_fin),
            ('move_type', 'in', ['out_invoice', 'out_refund']),
        ]
        
        if diario:
            domain.append(('journal_id', 'in', diario))
        if comercial:
            domain.append(('invoice_user_id', 'in', comercial))
        if cashier:
            domain.append(('pos_order_ids.employee_id', 'in', cashier))
            
        invoices = self.env['account.move'].search(domain)
        
        if invoices:
            for invoice in invoices:
                data_detail = {}
                date_formated = datetime.strftime(invoice.date, "%d/%m/%Y") 

                data_detail['fecha'] = date_formated
                data_detail['numero'] = invoice.name
                data_detail['diario_contable'] = invoice.journal_id.name
                data_detail['comercial'] = invoice.invoice_user_id.partner_id.name
                data_detail['pos'] = invoice.pos_order_ids.employee_id.name or ""
                data_detail['cliente'] = invoice.partner_id.name or ""
                data_detail['subtotal'] = abs(invoice.amount_untaxed_signed)
                data_detail['iva'] = abs(invoice.amount_tax)
                data_detail['total'] = abs(invoice.amount_total_signed)
                data_detail['cash'] = 0
                data_detail['bank'] = 0
                data_detail['receivable'] = 0
                
                if invoice.move_type == 'out_invoice':
                    data_detail['tipo'] = 'Factura'
                    
                elif invoice.move_type == 'out_refund':
                    data_detail['tipo'] = 'Nota de crédito'
                    data_detail['subtotal'] = - data_detail['subtotal']
                    data_detail['iva'] = - data_detail['iva']
                    data_detail['total'] = - data_detail['total']
                
                payment_widget = invoice.invoice_payments_widget
                
                if payment_widget:
                    contents = payment_widget['content']
                    for content in contents:
                        pos_payment_name = content.get('pos_payment_name', None)
                        content_amount = content.get('amount', 0)
                        partial_id = content.get('partial_id', 0)
                        if not pos_payment_name:
                            journal_name = content['journal_name']

                            journal = self.env['account.journal'].search([('name', '=', journal_name)], limit=1)                           
                            
                            if journal.type == 'cash':
                                # Sumar el monto si el método ya existe
                                data_detail['cash'] += content_amount
                                
                            elif journal.type == 'bank':
                                data_detail['bank'] += content_amount
                                
                            else:
                                reconcile_id = self.env['account.partial.reconcile'].search([('id', '=', partial_id)])
                                
                                if reconcile_id:
                                    debit_move = reconcile_id.debit_move_id
                                    
                                    _logger.info(f"""
                                                 
                                                 MOVE ID    :   { debit_move.move_id }      |
                                                 JOURNAL ID :   { debit_move.journal_id }   |
                                                 LINE ID    :   { debit_move.id }           |
                                                 
                                                 """)
                                
                                
                                id = content.get('move_id', None)
                                move_id = self.env['account.move'].search([('id', '=', id)])
                                
                                if move_id:
                                    _logger.info(f'MOSTRANDO CREDIT DEBIT >>> { move_id.invoice_outstanding_credits_debits_widget }')
                                    lines = move_id.line_ids.filtered(lambda line : line.debit > 0)
                                    
                                    if lines:
                                        for line in lines:
                                            _logger.info(f'MOSTRANDO PAGOS >>> { line.matched_credit_ids  }')
                                            name = line.name
                                            _logger.info(f'MOSTRANDO NAME >>> { name }')
                                            payment_name = name
                                
                                            pos_payment = self.env['pos.payment.method'].search([('name', '=', payment_name)])
                                            journal = pos_payment.journal_id
                                        
                                            if journal.type == 'cash':
                                                # Sumar el monto si el método ya existe
                                                data_detail['cash'] += content_amount
                                                
                                            elif journal.type == 'bank':
                                                data_detail['bank'] += content_amount
    
                                                      
                        else:                            
                            pos_payment = self.env['pos.payment.method'].search([('name', '=', pos_payment_name)])
                            journal = pos_payment.journal_id
                            
                            if journal.type == 'cash':
                                # Sumar el monto si el método ya existe
                                data_detail['cash'] += content_amount
                                
                            elif journal.type == 'bank':
                                data_detail['bank'] += content_amount
                                
                            # data_detail[ journal.type ] = content['amount']
                
                # else:
                #     pos_order = invoice.pos_order_ids
                    
                #     _logger.info(f'CONTIENE POS_ORDER SEGUNDO ELSE >>>> { pos_order }')
                    
                #     # Se evalua el metodo de pago (cuenta por cobrar) no contiene journal_type
                #     if pos_order:
                #         for payment in pos_order.payment_ids:
                #             data_detail['receivable'] = payment.amount
              
                monto_cuenta_por_cobrar = round((data_detail['cash'] + data_detail['bank']),2)                
                data_detail['receivable'] = round((data_detail['total'] - monto_cuenta_por_cobrar),2)
                
                data_invoice_details.append(data_detail)
            
                # _logger.info(f'MOSTRANDO DATA INVOICE DETAIL >>> { data_detail }')
               
            return data_invoice_details
        
        else:
            raise ValidationError("¡No se encontraron registros para los criterios dados!")  