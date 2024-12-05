import io
import json
from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

class AccountDueWizard(models.TransientModel):
    _name = "account.due.wizard"
    _description = "Cuentas por Cobrar Vencidas"
    
    court_date = fields.Date(
        string = 'Fecha de corte',
        help = 'Fecha de corte para analizar el informe',
        required = True
    )
    
    client_id = fields.Many2one(
        string='Cliente',
        comodel_name='res.partner',
        
        domain=[
            ('type','!=','private'),
            ('company_id','=',False),
        ]
    )
    
    journal_id = fields.Many2one(
        string = 'Diario',
        comodel_name='account.journal',
        domain=[('type','=','sale')] 
    )
    
    comercial_id = fields.Many2one(
        string = 'Comercial',
        comodel_name='res.users'
    )
    
    report_type = fields.Selection(
        [
            ('r', 'Resumido'),
            ('d', 'Detallado')
        ],
        string = 'Informe',
        default = 'r',
        help = "Seleccione el tipo de informe a visualizar"
    )
    
    def get_report_data(self):
        data_invoice_details = []
        court_date = self.court_date
        client_id = self.client_id.id
        journal_id = self.journal_id.id
        comercial_id = self.comercial_id.id
        
        domain = [
            ('move_id.invoice_date_due', '<=', court_date),
            ('amount_residual', '>', 0),
            ('partner_id', '=', client_id),
            ('move_id.move_type', 'in', ['out_invoice']),
            ('move_id.payment_state', 'in', ['not_paid', 'partial']),
            ('account_id.account_type', '=', 'asset_receivable'),
            ('parent_state', '=', 'posted'),
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
            
            data = {
                'result_data': data_invoice_details,
            }
            
            return data
        
        else:
            raise ValidationError("¡No se encontraron registros para los criterios dados!")   
    
    def action_pdf(self):
        data = {
            'model_id': self.id,
            'court_date': self.court_date,
            'client_id': self.client_id.id,
            'journal_id': self.journal_id.id,
            'comercial_id': self.comercial_id.id,
            'is_summary': self.report_type
        }
        
        return (
            self.env.ref(
                'account_due.report_account_due_action'
            )
            .report_action(None, data=data)
        )
    
    def action_excel(self):
        """This function is for printing excel report"""
        data = self.get_report_data()
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'account.due.wizard',
                     'options': json.dumps(
                         data, default=fields.date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'reporte_cuentas_por_cobrar',
                     },
            'report_type': 'xlsx',
        }
        
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
        sheet.merge_range('A1:M1', 'Informe de Facturas y Notas de Crédito', title_format)
            
        # Encabezados
        headers = [
            'Vencido por cobrar',
            'Fecha vencimiento',
            'Importe en moneda',
            'En fecha',
            '1 - 30',
            '31 - 60',
            '61 - 90',
            '91 - 120',
            'Más antiguos',
            'Total',
        ]
        
        for col, header in enumerate(headers):
            sheet.merge_range(2, col, 3, col, header, header_format)
                
            header_length = len(header)  # Longitud del encabezado
            sheet.set_column(col, col, header_length + 5)
        
        # Escribir datos
        row = 4  # Comenzar desde la fila 3 después de los encabezados
        for val in datas:
            sheet.write(row, 0, val['invoice'], text_format)
            sheet.write(row, 1, val['date_due'], text_format)
            sheet.write(row, 2, val['amount_residual'], text_format)
            sheet.write(row, 3, val.get('actual') if val.get('actual') else '', text_format)
            sheet.write(row, 4, val.get('1 - 30') if val.get('1 - 30') else '', text_format)
            sheet.write(row, 5, val.get('31 - 60') if val.get('31 - 60') else '', text_format)
            sheet.write(row, 6, val.get('61 - 90') if val.get('61 - 90') else '', text_format)
            sheet.write(row, 7, val.get('91 - 120') if val.get('91 - 120') else '', text_format)
            sheet.write(row, 8, val.get('antiguo') if val.get('antiguo') else '', text_format)
            sheet.write(row, 9, 0, text_format)
            
            row += 1

        # Cerrar el libro
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
   