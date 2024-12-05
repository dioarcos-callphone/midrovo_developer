from odoo import models, api
from odoo.exceptions import ValidationError
from datetime import datetime

class InvoiceDetails(models.AbstractModel):
    _name = 'report.account_due.report_account_due'
    _description = 'Reporte de Detalles de Facturas'
    
    @api.model
    def _get_report_values(self, docids, data=None):
        account_move_lines = []
        court_date = data['court_date']
        client_id = data['client_id']
        journal_id = data['journal_id']
        comercial_id = data['comercial_id']
        is_summary = data['is_summary']
        
        if is_summary == 'r':
            return {
                'doc_ids': docids,
                'doc_model': 'report.account_due.report_account_due',
                'data': data,
                'is_summary': is_summary,
                'options': self.get_residual_totals(court_date),
            }

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
        # if journal_id:
        #     domain.append(('journal_id', '=', journal_id))
        # if comercial_id:
        #     domain.append(('move_id.invoice_user_id', '=', comercial_id))
        
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
                data_detail['journal'] = detail.journal_id.id
                data_detail['comercial'] = detail.move_id.invoice_user_id.partner_id.id
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
            
            account_move_lines_filtered = []
            
            filters = []
            if journal_id:
                filters.append(lambda x: x.get('journal') == journal_id)
            if comercial_id:
                filters.append(lambda x: x.get('comercial') == comercial_id)

            # Aplica los filtros si hay alguno
            if filters:
                account_move_lines_filtered = [
                    line for line in account_move_lines if all(f(line) for f in filters)
                ]
            else:
                account_move_lines_filtered = account_move_lines

            accounts_receivable_data = {
                'client': client.name,
                'actual': actual,
                'periodo1': periodo_1,
                'periodo2': periodo_2,
                'periodo3': periodo_3,
                'periodo4': periodo_4,
                'antiguo': antiguo,
                'total': total,
                'lines': account_move_lines_filtered
            }
            
            # if journal_id:
            #     account_move_lines_filtered = list(
            #         filter(
            #             lambda x: x.get('journal') == journal_id,
            #             account_move_lines
            #         )
            #     )
            
            # if journal_id and comercial_id:
            #     account_move_lines_filtered = list(
            #         filter(
            #             lambda x: x.get('journal') == journal_id and x.get('comercial') == comercial_id,
            #             account_move_lines
            #         )
            #     )
            
            # elif journal_id:
            #     account_move_lines_filtered = list(
            #         filter(
            #             lambda x: x.get('journal') == journal_id,
            #             account_move_lines
            #         )
            #     )
                
            # elif comercial_id:
            #     account_move_lines_filtered = list(
            #         filter(
            #             lambda x: x.get('comercial') == comercial_id,
            #             account_move_lines
            #         )
            #     )                
            
            # accounts_receivable_data = {
            #     'client': client.name,
            #     'actual': actual,
            #     'periodo1': periodo_1,
            #     'periodo2': periodo_2,
            #     'periodo3': periodo_3,
            #     'periodo4': periodo_4,
            #     'antiguo': antiguo,
            #     'total': total,
            #     'lines': account_move_lines if not journal_id or not comercial_id else account_move_lines_filtered
            # }
            
            return {
                'doc_ids': docids,
                'doc_model': 'report.account_due.report_account_due',
                'data': data,
                'is_summary': is_summary,
                'options': accounts_receivable_data,
            }
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
    