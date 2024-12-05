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
        account_move_lines = []
        court_date = self.court_date
        client_id = self.client_id.id
        journal_id = self.journal_id.id
        comercial_id = self.comercial_id.id
        
        if self.report_type == 'r':
            data = {
                'result_data': self.get_residual_totals(court_date),
                'is_summary': self.report_type,
            }
            
            return data
        
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
            actual = 0
            periodo_1 = 0
            periodo_2 = 0
            periodo_3 = 0
            periodo_4 = 0
            antiguo = 0
                 
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
                data_detail['periodo1'] = False
                data_detail['periodo2'] = False
                data_detail['periodo3'] = False
                data_detail['periodo4'] = False
                data_detail['antiguo'] = False
                
                fecha_vencida = detail.move_id.invoice_date_due
                fecha_actual = datetime.now()
                
                dias_transcurridos = (fecha_actual.date() - fecha_vencida).days
                
                # Determinar el rango
                if dias_transcurridos == 0:
                    data_detail['actual'] = data_detail['amount_residual']
                    actual += data_detail['actual']
                elif dias_transcurridos <= 30:
                    data_detail['periodo1'] = data_detail['amount_residual']
                    periodo_1 += data_detail['periodo1']
                elif dias_transcurridos <= 60:
                    data_detail['periodo2'] = data_detail['amount_residual']
                    periodo_2 += data_detail['periodo2']
                elif dias_transcurridos <= 90:
                    data_detail['periodo3'] = data_detail['amount_residual']
                    periodo_3 += data_detail['periodo3']
                elif dias_transcurridos <= 120:
                    data_detail['periodo4'] = data_detail['amount_residual']
                    periodo_4 += data_detail['periodo4']
                else:
                    data_detail['antiguo'] = data_detail['amount_residual']
                    antiguo += data_detail['antiguo']
  
                account_move_lines.append(data_detail)
            
            client = self.env['res.partner'].search([('id', '=', client_id)], limit=1)
            
            actual = round(actual, 2)
            
            periodo_1 = round(periodo_1, 2)
            periodo_2 = round(periodo_2, 2)
            periodo_3 = round(periodo_3, 2)
            periodo_4 = round(periodo_4, 2)
            antiguo = round(antiguo, 2)
            
            numbers = [actual, periodo_1, periodo_2, periodo_3, periodo_4]
            
            total = round(sum(numbers), 2)
                
            accounts_receivable_data = {
                'client': client.name,
                'actual': actual,
                'periodo1': periodo_1,
                'periodo2': periodo_2,
                'periodo3': periodo_3,
                'periodo4': periodo_4,
                'antiguo': antiguo,
                'total': total,
                'lines': account_move_lines,
            }
            
            data = {
                'result_data': accounts_receivable_data,
                'is_summary': self.report_type,
            }
            
            return data
        
        else:
            raise ValidationError("¡No se encontraron registros para los criterios dados!")   
    
    
    def get_residual_totals(self, date_due):
        # Filtrar líneas contables
        move_lines = self.env['account.move.line']

        # Agrupación y suma usando read_group
        results = move_lines.read_group(
            domain=[
                ('move_id.invoice_date_due', '<=', date_due),
                ('amount_residual', '!=', 0),
                ('move_id.move_type', 'in', ['out_invoice', 'out_refund', 'entry']),
                ('move_id.payment_state', 'in', ['not_paid', 'partial']),
                ('account_id.account_type', '=', 'asset_receivable'),
                ('parent_state', '=', 'posted'),
            ],
            fields=['partner_id', 'amount_residual:sum'],
            groupby=['partner_id'],
        )
        
        if results:
            processed_results = []

            for group in results:
                partner_id = group['partner_id'][0]  # ID del cliente
                processed_results.append({
                    'partner_id': partner_id,
                    'amount_residual': group['amount_residual'],
                    'partner_id_count': group['partner_id_count'],
                })
                
            summary_account_move_lines = []
                
            for result in processed_results:
                partner_id = result.get('partner_id')
                
                partner = self.env['res.partner'].browse(partner_id).name
                
                lines = move_lines.search([
                    ('move_id.invoice_date_due', '<=', date_due),
                    ('amount_residual', '!=', 0),
                    ('move_id.move_type', 'in', ['out_invoice', 'out_refund', 'entry']),
                    ('move_id.payment_state', 'in', ['not_paid', 'partial']),
                    ('account_id.account_type', '=', 'asset_receivable'),
                    ('parent_state', '=', 'posted'),
                    ('partner_id', '=', partner_id),
                ])
                
                if lines:
                    actual = 0
                    periodo_1 = 0
                    periodo_2 = 0
                    periodo_3 = 0
                    periodo_4 = 0
                    antiguo = 0
                    
                    for line in lines:
                        fecha_vencida = line.move_id.invoice_date_due
                        
                        fecha_actual = datetime.now()
                        
                        dias_transcurridos = (fecha_actual.date() - fecha_vencida).days
                        
                        # Determinar el rango
                        if dias_transcurridos == 0:
                            actual += line.amount_residual
                        elif dias_transcurridos <= 30:
                            periodo_1 += line.amount_residual
                        elif dias_transcurridos <= 60:
                            periodo_2 += line.amount_residual
                        elif dias_transcurridos <= 90:
                            periodo_3 += line.amount_residual
                        elif dias_transcurridos <= 120:
                            periodo_4 += line.amount_residual
                        else:
                            antiguo += line.amount_residual
                            
                    actual = round(actual, 2)
                
                    periodo_1 = round(periodo_1, 2)
                    periodo_2 = round(periodo_2, 2)
                    periodo_3 = round(periodo_3, 2)
                    periodo_4 = round(periodo_4, 2)
                    antiguo = round(antiguo, 2)
                    
                    numbers = [actual, periodo_1, periodo_2, periodo_3, periodo_4]
                    
                    total = round(sum(numbers), 2)
                            
                    summary_account_move_lines.append({
                        'cliente': partner,
                        'actual': actual,
                        'periodo1': periodo_1,
                        'periodo2': periodo_2,
                        'periodo3': periodo_3,
                        'periodo4': periodo_4,
                        'antiguo': antiguo,
                        'total': total,
                    })

            return summary_account_move_lines
        
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
        
        _logger.info(f'MOSTRANDO DATAS >>> { datas }')
        
        is_summary = data['is_summary']
        
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
        if is_summary == 'r':
            sheet.merge_range('A1:J1', 'Cuentas Vencidas por Cobrar (Resumido)', title_format)
            
        elif is_summary == 'd':    
            sheet.merge_range('A1:J1', 'Cuentas Vencidas por Cobrar (Detallado)', title_format)
            
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
        
        if is_summary == 'd':
            row = 4
            sheet.write(row, 0, val.get('client'), text_format)
            sheet.write(row, 1, '', text_format)
            sheet.write(row, 2, '', text_format)
            sheet.write(row, 3, val.get('actual') if val.get('actual') else '', text_format)
            sheet.write(row, 4, val.get('periodo1') if val.get('periodo1') else '', text_format)
            sheet.write(row, 5, val.get('periodo2') if val.get('periodo2') else '', text_format)
            sheet.write(row, 6, val.get('periodo3') if val.get('periodo3') else '', text_format)
            sheet.write(row, 7, val.get('periodo4') if val.get('periodo4') else '', text_format)
            sheet.write(row, 8, val.get('antiguo') if val.get('antiguo') else '', text_format)
            sheet.write(row, 9, val.get('total'), text_format)

            # Escribir datos
            row = 5  # Comenzar desde la fila 4 después de los encabezados
            
            lines = datas.get('lines')
            
            _logger.info(f'MOSTRANDO LINES >>> { lines }')
            
            for val in lines:
                sheet.write(row, 0, val.get('invoice'), text_format)
                sheet.write(row, 1, val.get('date_due'), text_format)
                sheet.write(row, 2, val.get('amount_residual'), text_format)
                sheet.write(row, 3, val.get('actual') if val.get('actual') else '', text_format)
                sheet.write(row, 4, val.get('periodo1') if val.get('periodo1') else '', text_format)
                sheet.write(row, 5, val.get('periodo2') if val.get('periodo2') else '', text_format)
                sheet.write(row, 6, val.get('periodo3') if val.get('periodo3') else '', text_format)
                sheet.write(row, 7, val.get('periodo4') if val.get('periodo4') else '', text_format)
                sheet.write(row, 8, val.get('antiguo') if val.get('antiguo') else '', text_format)
                sheet.write(row, 9, val.get('total'), text_format)
                
                row += 1
                
        elif is_summary == 'r':
            row = 4  # Comenzar desde la fila 4 después de los encabezados
            for val in datas:
                sheet.write(row, 0, val.get('cliente'), text_format)
                sheet.write(row, 1, '', text_format)
                sheet.write(row, 2, '', text_format)
                sheet.write(row, 3, val.get('actual') if val.get('actual') else '', text_format)
                sheet.write(row, 4, val.get('periodo1') if val.get('periodo1') else '', text_format)
                sheet.write(row, 5, val.get('periodo2') if val.get('periodo2') else '', text_format)
                sheet.write(row, 6, val.get('periodo3') if val.get('periodo3') else '', text_format)
                sheet.write(row, 7, val.get('periodo4') if val.get('periodo4') else '', text_format)
                sheet.write(row, 8, val.get('antiguo') if val.get('antiguo') else '', text_format)
                sheet.write(row, 9, val.get('total'), text_format)
                
                row += 1

        # Cerrar el libro
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
   