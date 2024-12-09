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
        ],
        required=True
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
            ('d', 'Detallado'),
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
            ('amount_residual', '!=', 0),
            ('move_id.move_type', 'in', ['out_invoice', 'out_refund', 'entry']),
            ('move_id.payment_state', 'in', ['not_paid', 'partial']),
            ('account_id.account_type', '=', 'asset_receivable'),
            ('parent_state', '=', 'posted'),
        ]
        
        if client_id:
            domain.append(('partner_id', '=', client_id))
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
            
            # Crear un diccionario para agrupar facturas por su id
            grouped_invoices = {}
            
            for detail in invoice_details:
                invoice_id = detail.move_id.id
                fecha_vencida = detail.move_id.invoice_date_due
                amount_residual = detail.amount_residual
                
                if invoice_id in grouped_invoices:
                    # Actualizar la fecha de vencimiento a la más reciente
                    if fecha_vencida > grouped_invoices[invoice_id]['date_due']:
                        grouped_invoices[invoice_id]['date_due'] = fecha_vencida
                    # Sumar el monto residual
                    grouped_invoices[invoice_id]['amount_residual'] += amount_residual
                    
                else:
                    # Crear una nueva entrada para la factura
                    grouped_invoices[invoice_id] = {
                        'date_due': fecha_vencida,
                        'invoice': detail.move_name,
                        'amount_residual': amount_residual,
                        'journal': detail.journal_id.id,
                        'comercial': detail.move_id.invoice_user_id.id,
                        'client': detail.partner_id.name or "",
                        'account': detail.account_id.code,
                        'actual': False,
                        'periodo1': False,
                        'periodo2': False,
                        'periodo3': False,
                        'periodo4': False,
                        'antiguo': False
                    }
                    
            # Procesar los datos agrupados
            for invoice_data in grouped_invoices.values():
                date_due = invoice_data['date_due']
                amount_residual = invoice_data['amount_residual']
                
                dias_transcurridos = (court_date - date_due).days

                # Determinar el rango
                if dias_transcurridos <= 0:
                    invoice_data['actual'] = amount_residual
                    actual += amount_residual
                elif dias_transcurridos <= 30:
                    invoice_data['periodo1'] = amount_residual
                    periodo_1 += amount_residual
                elif dias_transcurridos <= 60:
                    invoice_data['periodo2'] = amount_residual
                    periodo_2 += amount_residual
                elif dias_transcurridos <= 90:
                    invoice_data['periodo3'] = amount_residual
                    periodo_3 += amount_residual
                elif dias_transcurridos <= 120:
                    invoice_data['periodo4'] = amount_residual
                    periodo_4 += amount_residual
                else:
                    invoice_data['antiguo'] = amount_residual
                    antiguo += amount_residual
                    
                date_formated = datetime.strftime(date_due, "%d/%m/%Y")
                invoice_data['date_due'] = date_formated

                # Añadir al resultado final
                account_move_lines.append(invoice_data)
            
            client = self.env['res.partner'].search([('id', '=', client_id)], limit=1)
            
            actual = round(actual, 2)
            
            periodo_1 = round(periodo_1, 2)
            periodo_2 = round(periodo_2, 2)
            periodo_3 = round(periodo_3, 2)
            periodo_4 = round(periodo_4, 2)
            antiguo = round(antiguo, 2)
            
            numbers = [actual, periodo_1, periodo_2, periodo_3, periodo_4]
            
            total = round(sum(numbers), 2)
            
            account_move_lines_filtered = account_move_lines

            # if journal_id and comercial_id:
            #     # Filtrar por ambos campos
            #     account_move_lines_filtered = list(
            #         filter(
            #             lambda x: x.get('journal') == journal_id and x.get('comercial') == comercial_id,
            #             account_move_lines
            #         )
            #     )
            # elif journal_id:
            #     # Filtrar solo por journal_id
            #     account_move_lines_filtered = list(
            #         filter(
            #             lambda x: x.get('journal') == journal_id,
            #             account_move_lines
            #         )
            #     )
            # elif comercial_id:
            #     # Filtrar solo por comercial_id
            #     account_move_lines_filtered = list(
            #         filter(
            #             lambda x: x.get('comercial') == comercial_id,
            #             account_move_lines
            #         )
            #     )
                
            # if not account_move_lines_filtered:
            #     raise ValidationError("¡No se encontraron registros para los criterios dados!")  
                
            accounts_receivable_data = {
                'client': client.name,
                'actual': actual,
                'periodo1': periodo_1,
                'periodo2': periodo_2,
                'periodo3': periodo_3,
                'periodo4': periodo_4,
                'antiguo': antiguo,
                'total': total,
                'lines': account_move_lines_filtered,
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
                        if dias_transcurridos <= 0:
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
            sheet.write(row, 0, datas.get('client'), text_format)
            sheet.write(row, 1, '', text_format)
            sheet.write(row, 2, '', text_format)
            sheet.write(row, 3, datas.get('actual') if datas.get('actual') != 0 else '', text_format)
            sheet.write(row, 4, datas.get('periodo1') if datas.get('periodo1') != 0 else '', text_format)
            sheet.write(row, 5, datas.get('periodo2') if datas.get('periodo2') != 0 else '', text_format)
            sheet.write(row, 6, datas.get('periodo3') if datas.get('periodo3') != 0 else '', text_format)
            sheet.write(row, 7, datas.get('periodo4') if datas.get('periodo4') != 0 else '', text_format)
            sheet.write(row, 8, datas.get('antiguo') if datas.get('antiguo') != 0 else '', text_format)
            sheet.write(row, 9, datas.get('total'), text_format)
            
            row = 5
            
            lines = datas.get('lines')
            
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
                sheet.write(row, 9, '', text_format)
                
                row += 1
                
        elif is_summary == 'r':
            row = 4  # Comenzar desde la fila 4 después de los encabezados
            for line in datas:
                sheet.write(row, 0, line.get('cliente'), text_format)
                sheet.write(row, 1, '', text_format)
                sheet.write(row, 2, '', text_format)
                sheet.write(row, 3, line.get('actual') if line.get('actual') != 0 else '', text_format)
                sheet.write(row, 4, line.get('periodo1') if line.get('periodo1') != 0 else '', text_format)
                sheet.write(row, 5, line.get('periodo2') if line.get('periodo2') != 0 else '', text_format)
                sheet.write(row, 6, line.get('periodo3') if line.get('periodo3') != 0 else '', text_format)
                sheet.write(row, 7, line.get('periodo4') if line.get('periodo4') != 0 else '', text_format)
                sheet.write(row, 8, line.get('antiguo') if line.get('antiguo') != 0 else '', text_format)

                sheet.write(row, 9, line.get('total'), text_format)
                
                row += 1

        # Cerrar el libro
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
   