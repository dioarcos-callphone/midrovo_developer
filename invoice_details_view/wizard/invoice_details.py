import io
import json
from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

import logging
_logger = logging.getLogger(__name__)
        
class InvoiceDetails(models.TransientModel):
    _name = "invoice.details.wizard"
    _description = "Informe de Detalles de las Facturas"
    
    start_date = fields.Date(
        string = 'Fecha de inicio',
        help = 'Fecha de inicio para analizar el informe',
        required = True
    )
    
    end_date = fields.Date(
        string = 'Fecha de fin',
        help = 'Fecha de fin para analizar el informe',
        required = True
    )
    
    journal_ids = fields.Many2many(
        string = 'Diario',
        comodel_name='account.journal',
        domain=[('type','=','sale')]
        
    )
    
    comercial_ids = fields.Many2many(
        string = 'Comercial',
        comodel_name='res.users'
    )
    
    cashier_ids = fields.Many2many(
        string = 'Vendedor',
        comodel_name='hr.employee'
    )
    
    cost_options = fields.Selection(
        [
            ('master', 'Costo Maestro'),
            ('movement', 'Costo Movimiento')
        ],
        string = 'Costo',
        default = 'master',
        help="""Costo Maestro para el costo precio estandar del producto, Costo Movimiento para el debito de la línea de factura."""        
    )
    
    informe = fields.Selection(
        [
            ('r', 'Resumido'),
            ('d', 'Detallado')
        ],
        string = 'Informe',
        default = 'r',
        help = """Seleccione el tipo de informe a visualizar"""
    )
    
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
                data_detail['diario_contable'] = invoice.journal_id.name,
                data_detail['comercial'] = invoice.invoice_user_id.partner_id.name,
                data_detail['pos'] = invoice.pos_order_ids.employee_id.name,
                data_detail['cliente'] = invoice.partner_id.name,
                data_detail['subtotal'] = invoice.amount_untaxed_signed,
                data_detail['iva'] = invoice.amount_tax,
                data_detail['total'] = invoice.amount_total_signed
                
                if invoice.move_type == 'out_invoice':
                    data_detail['tipo'] = 'Factura'
                    
                elif invoice.move_type == 'out_refund':
                    data_detail['subtotal'] = - invoice.amount_untaxed_signed,
                    data_detail['iva'] = - invoice.amount_tax,
                    data_detail['total'] = - invoice.amount_total_signed
                
                methods = self.env['pos.payment.method'].search_read([], ['name'])
                pos_order = invoice.pos_order_ids
                
                for method in methods:
                    data_detail[method['name']] = 0
                    if pos_order:
                        for payment in pos_order.payment_ids:
                            if method['name'] == payment.payment_method_id.name:
                                data_detail[method['name']] = payment.amount
                    else:
                        if invoice.invoice_payments_widget:
                            content = invoice.invoice_payments_widget['content']
                            
                            for c in content:
                                if method['name'] == c['journal_name']:
                                    data_detail[method['name']] = c['amount']
                                    
                data_invoice_details.append(data_detail)
            
            return data_invoice_details
        
        else:
            raise ValidationError("¡No se encontraron registros para los criterios dados!")  
    
    # Esta funcion se vincula con action_excel genera los datos que van a ser expuestos en el excel
    def get_report_data(self):
        if self.start_date > self.end_date:
            raise ValidationError("La fecha de inicio no puede ser mayor que la fecha de fin")
                
        data_invoice_details = []
        fecha_inicio = self.start_date
        fecha_fin = self.end_date
        diario = self.journal_ids.ids
        comercial = self.comercial_ids.ids
        cashier = self.cashier_ids.ids
        
        if self.informe == 'r':
            data_invoices = self.get_report_facturas(fecha_inicio, fecha_fin, comercial, cashier, diario)
            data = {
                'result_data': data_invoices,
                'is_resumen': self.informe,
            }
            
            _logger.info(f'MOSTRANDO DATA >>> { data }')
            return data
            
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
        
        # condiciones de dominio de acuerdo a los filtros que selecciona el usuario
        if diario:
            domain.append(('journal_id', 'in', diario))
        if comercial:
            domain.append(('move_id.invoice_user_id', 'in', comercial))
        if cashier:
            domain.append(('move_id.pos_order_ids.employee_id', 'in', cashier))
        
        # trae las lineas de factura en base al dominio que se le establece
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
                
                product = detail.product_id

                # Inicializar las variables y asignar N/A si no se encuentra
                marca = next((v.name for v in product.product_template_variant_value_ids if v.attribute_id.name.lower() in ['marca', 'marcas']), "N/A")
                talla = next((v.name for v in product.product_template_variant_value_ids if v.attribute_id.name.lower() in ['talla', 'tallas']), "N/A")
                color = next((v.name for v in product.product_template_variant_value_ids if v.attribute_id.name.lower() in ['color', 'colores']), "N/A")
                material = next((v.name for v in product.product_template_variant_value_ids if v.attribute_id.name.lower() in ['material', 'materiales']), "N/A")
                material_capellada = next((v.name for v in product.product_template_variant_value_ids if v.attribute_id.name.lower() in ['material capellada']), "N/A")
                pais = next((v.name for v in product.product_template_variant_value_ids if v.attribute_id.name.lower() in ['país de origen']), "N/A")
                tipo_calzado = next((v.name for v in product.product_template_variant_value_ids if v.attribute_id.name.lower() in ['tipo de calzado']), "N/A")

                # Buscar en attribute_line_ids solo si no se encontraron los valores
                if (
                    color == "N/A" or
                    talla == "N/A" or
                    marca == "N/A" or
                    material == "N/A" or
                    material_capellada == "N/A" or
                    pais == "N/A" or
                    tipo_calzado == "N/A"
                ):
                    for attribute_line in product.product_tmpl_id.attribute_line_ids:
                        for value in attribute_line.value_ids:
                            if color == "N/A" and attribute_line.attribute_id.name.lower() in ['color', 'colores']:
                                color = value.name
                            
                            if talla == "N/A" and attribute_line.attribute_id.name.lower() in ['talla', 'tallas']:
                                talla = value.name
                            
                            if marca == "N/A" and attribute_line.attribute_id.name.lower() in ['marca', 'marcas']:
                                marca = value.name
                                
                            if material == "N/A" and attribute_line.attribute_id.name.lower() in ['material', 'materiales']:
                                material = value.name
                                
                            if material_capellada == "N/A" and attribute_line.attribute_id.name.lower() in ['material capellada']:
                                material_capellada = value.name
                                
                            if pais == "N/A" and attribute_line.attribute_id.name.lower() in ['país de origen']:
                                pais = value.name
                            
                            if tipo_calzado == "N/A" and attribute_line.attribute_id.name.lower() in ['tipo de calzado']:
                                tipo_calzado = value.name
                                
                descuento = round(0.00, 2)
                subtotal = detail.price_unit * detail.quantity
                
                if detail.discount:
                    descuento = round((subtotal * (detail.discount/100)),2)
                
                if self.cost_options == 'master':
                    total_costo = round((detail.product_id.standard_price * detail.quantity), 2)
                    
                if self.cost_options == 'movement':
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
                data_detail['marca'] = marca
                data_detail['talla'] = talla
                data_detail['color'] = color
                data_detail['material'] = material
                data_detail['material_capellada'] = material_capellada
                data_detail['pais'] = pais
                data_detail['tipo_calzado'] = tipo_calzado
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
                        if detail.move_id.invoice_payments_widget:
                            content = detail.move_id.invoice_payments_widget['content']
                            
                            for c in content:
                                if method['name'] == c['journal_name']:
                                    data_detail[method['name']] = c['amount']

                data_invoice_details.append(data_detail)
            
            data = {
                'result_data': data_invoice_details,
                'is_cost_or_debit': self.cost_options,
            }
            _logger.info(f'MOSTRANDO DATA >>> { data }')
            return data
        
        else:
            raise ValidationError("¡No se encontraron registros para los criterios dados!")    
        
    # Esta funcion retorna valores del filtro wizard a la funcion get_values
    # permitiendo generar el reporte en PDF
    def action_pdf(self):
        if self.start_date > self.end_date:
            raise ValidationError("La fecha de inicio no puede ser mayor que la fecha de fin")
        
        data = {
            'model_id': self.id,
            'fecha_inicio': self.start_date,
            'fecha_fin': self.end_date,
            'diario': self.journal_ids.ids,
            'comercial': self.comercial_ids.ids,
            'cashier': self.cashier_ids.ids,
            'is_cost_or_debit': self.cost_options
        }
        
        return (
            self.env.ref(
                'invoice_details_view.report_invoice_details_action'
            )
            .report_action(None, data=data)
        )
        
    def action_excel(self):
        """This function is for printing excel report"""
        data = self.get_report_data()
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'invoice.details.wizard',
                     'options': json.dumps(
                         data, default=fields.date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'reporte_detalle_facturas',
                     },
            'report_type': 'xlsx',
        }

    # Formato de hoja de Excel para imprimir los datos
    def get_xlsx_report(self, data, response):
        datas = data['result_data']
        is_cost_or_debit = data.get('is_cost_or_debit', None)
        is_resumen = data.get('is_resumen', None)
        
        _logger.info(f'MOSTRANDO INFORME >>> { is_resumen }')
        
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        
        # Configurar márgenes
        sheet.set_margins(0.5, 0.5, 0.5, 0.5)
        
        # Definición de estilos
        header_format = workbook.add_format({
            'font_name': 'Times New Roman',
            'bold': True,
            'bg_color': '#f2f2f2',  # Color de fondo gris claro para los encabezados
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })
        
        text_format = workbook.add_format({
            'font_name': 'Times New Roman',
            'border': 1,
            'align': 'left',
            'valign': 'vcenter'
        })
        
        title_format = workbook.add_format({
            'font_name': 'Times New Roman',
            'bold': True,
            'font_size': 16,
            'align': 'center',
            'valign': 'vcenter'
        })

        title_format_method = workbook.add_format({
            'font_name': 'Times New Roman',
            'border': 1,
            'bold': True,
            'font_size': 14,
            'align': 'center',
            'valign': 'vcenter'
        })
        title_format_method.set_rotation(90)

        # Título del informe
        if not self.env.user.has_group('invoice_details_view.group_invoice_details_view_user'):
            sheet.merge_range('A1:V1', 'Informe de Detalles de Facturas y Notas de Crédito', title_format)
        else:
            sheet.merge_range('A1:S1', 'Informe de Detalles de Facturas y Notas de Crédito', title_format)

        # Encabezados
        headers = [
            'Fecha',
            'Número',
            'Diario contable',
            'Tipo de documento',
            'Comercial',
            'Cajero',
            'Cliente',
        ]
        
        if is_resumen == 'r':
            headers.append('Subtotal')
            headers.append('Iva')
            headers.append('Total')
            headers.append('Efectivo')
            headers.append('Banco')
            headers.append('Cuenta de cliente')
            
        if is_resumen == None:
            headers.append('Producto')
            headers.append('Marca')
            headers.append('Talla')
            headers.append('Color')
            headers.append('Material')
            headers.append('Material capellada')
            headers.append('Tipo de calzado')
            headers.append('País de origen')
            headers.append('Cantidad')
            headers.append('Precio')
            headers.append('Descuento')
            headers.append('Subtotal')
            headers.append('Efectivo')
            headers.append('Banco')
            headers.append('Cuenta de cliente')

            if not self.env.user.has_group('invoice_details_view.group_invoice_details_view_user'):
                headers.append('Costo')
                headers.append('Total Costo')
                headers.append('Rentabilidad')
        
        for col, header in enumerate(headers):
            #sheet.write(2, col, header, header_format)
            if header == 'Costo' or header == 'Total Costo' or header == 'Rentabilidad':
                if not self.env.user.has_group('invoice_details_view.group_invoice_details_view_user'):
                    sheet.merge_range(2, col, 3, col, header, header_format)
                
            else:
                sheet.merge_range(2, col, 3, col, header, header_format)
                
            header_length = len(header)  # Longitud del encabezado
            sheet.set_column(col, col, header_length + 5)
            
            if header == 'Fecha' or header == 'Cajero':
                sheet.set_column(col, col, header_length + 6) 
                
            if header == 'Número' or header == 'Diario contable' or header == 'Producto':
                sheet.set_column(col, col, header_length + 18)
                
            if header == 'Comercial' or header == 'Cajero' or header == 'Cliente':
                sheet.set_column(col, col, header_length + 10)
        
        # Escribir datos
        row = 4  # Comenzar desde la fila 3 después de los encabezados
        for val in datas:
            sheet.write(row, 0, val['fecha'], text_format)
            sheet.write(row, 1, val['numero'], text_format)
            sheet.write(row, 2, val['diario_contable'], text_format)
            sheet.write(row, 3, val['tipo'], text_format)
            sheet.write(row, 4, val['comercial'], text_format)
            sheet.write(row, 5, val['pos'], text_format)
            sheet.write(row, 6, val['cliente'], text_format)
            
            if is_resumen == 'r':
                sheet.write(row, 7, val['subtotal'], text_format)
                sheet.write(row, 8, val['iva'], text_format)
                sheet.write(row, 9, val['total'], text_format)
                sheet.write(row, 10, val['Efectivo'], text_format)
                sheet.write(row, 11, val['Banco'], text_format)
                sheet.write(row, 12, val['Cuenta de cliente'], text_format)
            
            if is_resumen == None:
                sheet.write(row, 7, val['producto'], text_format)
                sheet.write(row, 8, val['marca'], text_format)
                sheet.write(row, 9, val['talla'], text_format)
                sheet.write(row, 10, val['color'], text_format)
                sheet.write(row, 11, val['material'], text_format)
                sheet.write(row, 12, val['material_capellada'], text_format)
                sheet.write(row, 13, val['tipo_calzado'], text_format)
                sheet.write(row, 14, val['pais'], text_format)
                sheet.write(row, 15, val['cantidad'], text_format)
                sheet.write(row, 16, val['precio'], text_format)
                sheet.write(row, 17, val['descuento'], text_format)
                sheet.write(row, 18, val['subtotal'], text_format)
                sheet.write(row, 19, val['Efectivo'], text_format)
                sheet.write(row, 20, val['Banco'], text_format)
                sheet.write(row, 21, val['Cuenta de cliente'], text_format)
            
                if not self.env.user.has_group('invoice_details_view.group_invoice_details_view_user'):
                    if is_cost_or_debit == 'master':
                        sheet.write(row, 22, val['costo'], text_format)
                    elif is_cost_or_debit == 'movement':
                        sheet.write(row, 22, val['debito'], text_format)
                    
                    sheet.write(row, 23, val['total_costo'], text_format)
                    sheet.write(row, 24, val['rentabilidad'], text_format)
            
            row += 1

        # Cerrar el libro
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
