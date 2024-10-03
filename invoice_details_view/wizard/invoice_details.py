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
    )
    
    comercial_ids = fields.Many2many(
        string = 'Comercial',
        comodel_name='res.users'
    )
    
    cashier_ids = fields.Many2many(
        string = 'Vendedor',
        comodel_name='hr.employee'
    )
    
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
        
        domain = [
            ('product_id', '!=', False),
            ('date', '>=', fecha_inicio),
            ('date', '<=', fecha_fin),
        ]
        
        # if diario:
        #     domain.append(('journal_id', 'in', diario))
        # if comercial:
        #     domain.append(('move_id.invoice_user_id', 'in', comercial))
        # if cashier:
        #     domain.append(('move_id.pos_order_ids.employee_id', 'in', cashier))
        
        invoice_details = self.env['account.move.line'].search(domain)
        
        if invoice_details:
            details_account_five = invoice_details.filtered(
                lambda d : d.account_id.code.startswith('5')
            )
            
            details_account_five = [{
                'id': d.id,
                'date': d.date,
                'move_id': d.move_id.id,
                'journal_id': d.journal_id.id,
                'account_id': d.account_id.id,
                'product_id': d.product_id.id,
                'move_name': d.move_name,
                'debit': d.debit,
                'quantity': abs(d.quantity)
            } for d in details_account_five]
            
            for detail in invoice_details:
                data_detail = {}
                debito = detail.debit
                for d_five in details_account_five:
                    if(
                        detail.date == d_five['date'] and
                        detail.product_id.id == d_five['product_id'] and
                        detail.quantity == d_five['quantity'] and
                        detail.journal_id.id == 1                        
                    ):
                        debito = round(d_five['debit'], 2)
                        
                        
                    # elif(
                    #     detail.date == d_five['date'] and
                    #     detail.product_id.id == d_five['product_id'] and
                    #     detail.quantity == d_five['quantity']
                    # ):
                    #     debito = round(d_five['debit'], 2)
                
                data_detail['debito'] = debito
            
            # for detail in invoice_details:
                descuento = round(0.00, 2)
                subtotal = detail.price_unit * detail.quantity
                if detail.discount:
                    descuento = round((subtotal * (detail.discount/100)),2)
                
                total_costo = round((detail.product_id.standard_price * detail.quantity), 2)
                rentabilidad = detail.price_subtotal - total_costo
                
                
                
                
            #     # product = detail.product_id
            #     # category = product.categ_id
            #     # account_five = category.property_stock_account_output_categ_id
                
            #     # d = self.env['account.move.line'].search([
            #     #     ('id', '=', detail.id),
            #     #     ('account_id', '=', account_five.id),
            #     # ])
                
            #     # _logger.info(f'MOSTRANDO CATEGORY >>> { d.debit }')
                
            #     # debit_detail = self.env['account.move.line'].search([
            #     #     ('id', '=', detail.id),
            #     #     ('account_id.code', 'like', '5%')
            #     # ])
                
            #     # _logger.info(f'MOSTRANDO LOS DEBIT DETAILS >>> { debit_detail.debit }')
                
            #     # _logger.info(f'MOVE ID >>> { detail.move_id }')
                
            #     line_ids = detail.move_id.line_ids
                
            #     for line in line_ids:
            #         _logger.info(f'MOSTRANDO LINEAS DE LA FACTURA >>> { line.debit }')
                
            #     _logger.info(f'MOSTRAR ACCOUNT >>>> { detail.move_id }')
                # if diario or comercial or cashier:
                #     if(
                #         detail.journal_id in diario or
                #         detail.move_id.invoice_user_id in comercial or
                #         detail.move_id.pos_order_ids.employee_id in cashier
                #     ):
                
                date_formated = datetime.strftime(detail.date, "%d/%m/%Y")
                
                data_detail['fecha'] = date_formated
                data_detail['numero'] = detail.move_name
                data_detail['comercial'] = detail.move_id.invoice_user_id.partner_id.name
                data_detail['pos'] = detail.move_id.pos_order_ids.employee_id.name or ""
                data_detail['cliente'] = detail.partner_id.name
                data_detail['producto'] = detail.product_id.name
                data_detail['cantidad'] = detail.quantity
                data_detail['precio'] = detail.price_unit
                data_detail['descuento'] = descuento
                data_detail['subtotal'] = detail.price_subtotal
                data_detail['costo'] = round(detail.product_id.standard_price, 2)
                data_detail['total_costo'] = total_costo
                data_detail['rentabilidad'] = round(rentabilidad, 2)
                
                # data_detail = {
                #     "fecha": date_formated,
                #     "numero": detail.move_name,
                #     "comercial": detail.move_id.invoice_user_id.partner_id.name,
                #     "pos": detail.move_id.pos_order_ids.employee_id.name or "",
                #     "cliente": detail.partner_id.name,
                #     "producto": detail.product_id.name,
                #     "cantidad": detail.quantity,
                #     "precio": detail.price_unit,
                #     "descuento": descuento,
                #     "subtotal": detail.price_subtotal,
                #     "costo": round(detail.product_id.standard_price, 2),
                #     "total_costo": total_costo,
                #     "rentabilidad": round(rentabilidad, 2),
                #     "debito": round(detail.credit, 2)
                # }
                if diario:
                    if detail.journal_id in diario:
                        data_invoice_details.append(data_detail)
                        
                if comercial:
                    if detail.move_id.invoice_user_id in comercial:
                        data_invoice_details.append(data_detail)
                
                if cashier:
                    if detail.move_id.pos_order_ids.employee_id in cashier:
                        data_invoice_details.append(data_detail)
            
            data = {
                'result_data': data_invoice_details,
            }
            return data
        
        else:
            raise ValidationError("No records found for the given criteria!")    
    
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
            'cashier': self.cashier_ids.ids
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
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx',
        }

    # Formato de hoja de Excel para imprimir los datos
    def get_xlsx_report(self, data, response):
        datas = data['result_data']
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

        # Título del informe
        sheet.merge_range('A1:M1', 'Informe de Detalles de Facturas', title_format)

        # Encabezados
        headers = [
            'Fecha',
            'Número',
            'Comercial',
            'Cajero',
            'Cliente',
            'Producto',
            'Cantidad',
            'Precio',
            'Descuento',
            'Subtotal',
            'Costo',
            'Total Costo',
            'Rentabilidad',
            'debito'
        ]
        for col, header in enumerate(headers):
            sheet.write(2, col, header, header_format)

        # Ajuste de columnas
        sheet.set_column('A:A', 22)  # Fecha
        sheet.set_column('B:B', 22)  # Número
        sheet.set_column('C:C', 20)  # Comercial
        sheet.set_column('D:D', 25)  # Cajero
        sheet.set_column('E:E', 25)  # Cliente
        sheet.set_column('F:F', 10)  # Product
        sheet.set_column('G:G', 10)  # Cantidad
        sheet.set_column('H:H', 11)  # Precio
        sheet.set_column('I:I', 10)  # Descuento
        sheet.set_column('J:J', 10)  # Subtotal
        sheet.set_column('K:K', 12)  # Costo
        sheet.set_column('L:L', 12)  # Total Costo
        sheet.set_column('M:M', 12)  # Rentabilidad
        sheet.set_column('N:N', 12)  # Debito

        # Escribir datos
        row = 3  # Comenzar desde la fila 3 después de los encabezados
        for val in datas:
            sheet.write(row, 0, val['fecha'], text_format)
            sheet.write(row, 1, val['numero'], text_format)
            sheet.write(row, 2, val['comercial'], text_format)
            sheet.write(row, 3, val['pos'], text_format)
            sheet.write(row, 4, val['numero'], text_format)
            sheet.write(row, 5, val['producto'], text_format)
            sheet.write(row, 6, val['cantidad'], text_format)
            sheet.write(row, 7, val['precio'], text_format)
            sheet.write(row, 8, val['descuento'], text_format)
            sheet.write(row, 9, val['subtotal'], text_format)
            sheet.write(row, 10, val['costo'], text_format)
            sheet.write(row, 11, val['total_costo'], text_format)
            sheet.write(row, 12, val['rentabilidad'], text_format)
            sheet.write(row, 13, val['debito'], text_format)
            row += 1

        # Cerrar el libro
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
