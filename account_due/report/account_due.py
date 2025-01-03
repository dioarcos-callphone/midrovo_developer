from odoo import models, api
from odoo.exceptions import ValidationError
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

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
        is_entry = data['is_entry']
        
        if is_summary == 'r':
            return {
                'doc_ids': docids,
                'doc_model': 'report.account_due.report_account_due',
                'data': data,
                'is_summary': is_summary,
                'options': self.get_residual_totals(data),
            }
            
        move_types = ['out_invoice', 'out_refund']
        
        if is_entry:
            move_types.append('entry')

        domain = [
            ('move_id.date', '<=', court_date),
            ('amount_residual', '!=', 0),
            ('move_id.move_type', 'in', move_types),
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
        
        invoice_details = self.env['account.move.line'].search(domain, order='move_name')
        
        if not client_id:
            # Agrupación y suma usando read_group
            results = invoice_details.read_group(
                domain=domain,
                fields=['partner_id', 'amount_residual:sum'],
                groupby=['partner_id'],
            )
            
            if results:
                processed_results = []

                for group in results:
                    partner_id = None  # O define un valor predeterminado
                    if isinstance(group.get('partner_id'), (list, tuple)) and group['partner_id']:
                        partner_id = group['partner_id'][0]  # ID del cliente                        

                    processed_results.append({
                        'partner_id': partner_id,
                        'amount_residual': group['amount_residual'],
                        'partner_id_count': group['partner_id_count'],
                    })
                
                result_final = []
                
                total_actual = 0
                total_periodo_1 = 0
                total_periodo_2 = 0
                total_periodo_3 = 0
                total_periodo_4 = 0
                total_antiguo = 0
                valor_total_adeudado = 0
                valor_total_vencido = 0
                    
                for result in processed_results:
                    domain.append(('partner_id', '=', result.get('partner_id', None)))
                    
                    partner = self.env['res.partner'].browse(result.get('partner_id', None)).name
                    
                    if not partner:
                        partner = 'Desconocido'
                    
                    account_move_line = self.env['account.move.line'].search(domain, order='move_name')
                    
                    if account_move_line:
                        data_lines = []
                        actual = 0
                        periodo_1 = 0
                        periodo_2 = 0
                        periodo_3 = 0
                        periodo_4 = 0
                        antiguo = 0
                        
                        grouped_invoices = {}
                        
                        for detail in account_move_line:
                            invoice_id = detail.move_id.id
                            fecha_vencida = detail.move_id.invoice_date_due
                            amount_residual = round(detail.amount_residual, 2)
                            
                            if invoice_id in grouped_invoices:
                                # Actualizar la fecha de vencimiento a la más reciente
                                if fecha_vencida > grouped_invoices[invoice_id]['date_due']:
                                    grouped_invoices[invoice_id]['date_due'] = fecha_vencida
                                # Sumar el monto residual
                                grouped_invoices[invoice_id]['amount_residual'] += round(amount_residual, 2)
                                
                            else:
                                # Crear una nueva entrada para la factura
                                grouped_invoices[invoice_id] = {
                                    'date_due': fecha_vencida,
                                    'invoice': detail.move_name,
                                    'date': datetime.strftime(detail.move_id.date, "%d/%m/%Y"),
                                    'count_days': (datetime.now().date() - detail.move_id.date).days,
                                    'amount_residual': round(amount_residual, 2),
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
                            amount_residual = round(invoice_data['amount_residual'], 2)
                            
                            court_date_date = datetime.strptime(court_date, '%Y-%m-%d')
                            
                            dias_transcurridos = (court_date_date.date() - date_due).days

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
                            data_lines.append(invoice_data)
                        
                        actual = round(actual, 2)
                        
                        periodo_1 = round(periodo_1, 2)
                        periodo_2 = round(periodo_2, 2)
                        periodo_3 = round(periodo_3, 2)
                        periodo_4 = round(periodo_4, 2)
                        antiguo = round(antiguo, 2)
                        
                        numbers = [actual, periodo_1, periodo_2, periodo_3, periodo_4, antiguo]
                        numbers_vencido = [periodo_1, periodo_2, periodo_3, periodo_4, antiguo]
                        
                        total = round(sum(numbers), 2)
                        total_vencido = round(sum(numbers_vencido), 2)
                        
                        account_move_lines_filtered = data_lines
                        
                        total_actual += actual
                        total_periodo_1 += periodo_1
                        total_periodo_2 += periodo_2
                        total_periodo_3 += periodo_3
                        total_periodo_4 += periodo_4
                        total_antiguo += antiguo
                        valor_total_adeudado += total
                        valor_total_vencido += total_vencido
                        
                        result_final.append({
                            'client': partner,
                            'actual': round(actual, 2),
                            'periodo1': round(periodo_1, 2),
                            'periodo2': round(periodo_2, 2),
                            'periodo3': round(periodo_3, 2),
                            'periodo4': round(periodo_4, 2),
                            'antiguo': round(antiguo, 2),
                            'total_adeudado': round(total, 2),
                            'total_vencido': round(total_vencido, 2),
                            'lines': account_move_lines_filtered
                        })
                        
                    domain.remove(('partner_id', '=', result.get('partner_id', None)))
                
                result_final.append({
                    'client': 'Total vencido por cobrar',
                    'actual': round(total_actual, 2),
                    'periodo1': round(total_periodo_1, 2),
                    'periodo2': round(total_periodo_2, 2),
                    'periodo3': round(total_periodo_3, 2),
                    'periodo4': round(total_periodo_4, 2),
                    'antiguo': round(total_antiguo, 2),
                    'total_adeudado': round(valor_total_adeudado, 2),
                    'total_vencido': round(valor_total_vencido, 2),
                    'lines': []
                })
                
                        
                return {
                    'doc_ids': docids,
                    'doc_model': 'report.account_due.report_account_due',
                    'data': data,
                    'is_summary': is_summary,
                    'options': result_final,
                }
        
        
        if invoice_details:
            actual = 0
            periodo_1 = 0
            periodo_2 = 0
            periodo_3 = 0
            periodo_4 = 0
            antiguo = 0
            
            # Crear un diccionario para agrupar facturas por su id
            grouped_invoices = {}
            
            result_final_detail = []
            
            for detail in invoice_details:
                invoice_id = detail.move_id.id
                fecha_vencida = detail.move_id.invoice_date_due
                amount_residual = round(detail.amount_residual, 2)
                
                if invoice_id in grouped_invoices:
                    # Actualizar la fecha de vencimiento a la más reciente
                    if fecha_vencida > grouped_invoices[invoice_id]['date_due']:
                        grouped_invoices[invoice_id]['date_due'] = fecha_vencida
                    # Sumar el monto residual
                    grouped_invoices[invoice_id]['amount_residual'] += round(amount_residual, 2)
                    
                else:
                    # Crear una nueva entrada para la factura
                    grouped_invoices[invoice_id] = {
                        'date_due': fecha_vencida,
                        'invoice': detail.move_name,
                        'date': datetime.strftime(detail.move_id.date, "%d/%m/%Y"),
                        'count_days': (datetime.now().date() - detail.move_id.date).days,
                        'amount_residual': round(amount_residual, 2),
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
                amount_residual = round(invoice_data['amount_residual'], 2)
                
                court_date_date = datetime.strptime(court_date, '%Y-%m-%d')
                
                dias_transcurridos = (court_date_date.date() - date_due).days

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
            
            numbers = [actual, periodo_1, periodo_2, periodo_3, periodo_4, antiguo]
            numbers_vencido = [periodo_1, periodo_2, periodo_3, periodo_4, antiguo]
            
            total = round(sum(numbers), 2)
            total_vencido = round(sum(numbers_vencido), 2)
            
            account_move_lines_filtered = account_move_lines
            
            result_final_detail.append({
                'client': client.name,
                'actual': round(actual, 2),
                'periodo1': round(periodo_1, 2),
                'periodo2': round(periodo_2, 2),
                'periodo3': round(periodo_3, 2),
                'periodo4': round(periodo_4, 2),
                'antiguo': round(antiguo, 2),
                'total_adeudado': round(total, 2),
                'total_vencido': round(total_vencido, 2),
                'lines': account_move_lines_filtered
            })
            
            return {
                'doc_ids': docids,
                'doc_model': 'report.account_due.report_account_due',
                'data': data,
                'is_summary': is_summary,
                'options': result_final_detail,
            }
        else:
            raise ValidationError("¡No se encontraron registros para los criterios dados!")

    
    def get_residual_totals(self, data=None):
        court_date = data['court_date']
        client_id = data['client_id']
        journal_id = data['journal_id']
        comercial_id = data['comercial_id']
        is_entry = data['is_entry']
        
        move_types = ['out_invoice', 'out_refund']
        
        if is_entry:
            move_types.append('entry')
        
        domain= [
            ('move_id.date', '<=', court_date),
            ('amount_residual', '!=', 0),
            ('move_id.move_type', 'in', move_types),
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
        
        # Filtrar líneas contables
        move_lines = self.env['account.move.line'].search(domain)
        
        summary_account_move_lines = []
        
        if not client_id:
            # Agrupación y suma usando read_group
            results = move_lines.read_group(
                domain=domain,
                fields=['partner_id', 'amount_residual:sum'],
                groupby=['partner_id'],
            )
            
            if results:
                processed_results = []

                for group in results:
                    partner_id = None  # O define un valor predeterminado
                    if isinstance(group.get('partner_id'), (list, tuple)) and group['partner_id']:
                        partner_id = group['partner_id'][0]  # ID del cliente   

                    processed_results.append({
                        'partner_id': partner_id,
                        'amount_residual': group['amount_residual'],
                        'partner_id_count': group['partner_id_count'],
                    })
                    
                total_actual = 0
                total_periodo_1 = 0
                total_periodo_2 = 0
                total_periodo_3 = 0
                total_periodo_4 = 0
                total_antiguo = 0
                valor_total_adeudado = 0
                valor_total_vencido = 0
                    
                for result in processed_results:
                    domain.append(('partner_id', '=', result.get('partner_id', None)))
                    
                    partner = self.env['res.partner'].browse(result.get('partner_id', None)).name
                    
                    if not partner:
                        partner = 'Desconocido'
                    
                    account_move_line = self.env['account.move.line'].search(domain)
                    
                    if account_move_line:
                        actual = 0
                        periodo_1 = 0
                        periodo_2 = 0
                        periodo_3 = 0
                        periodo_4 = 0
                        antiguo = 0
                        
                        for line in account_move_line:
                            fecha_vencida = line.move_id.invoice_date_due
                
                            court_date_date = datetime.strptime(court_date, '%Y-%m-%d')
                            
                            dias_transcurridos = (court_date_date.date() - fecha_vencida).days
                            
                            # dias_transcurridos = (fecha_actual.date() - fecha_vencida).days
                            
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
                        
                        numbers = [actual, periodo_1, periodo_2, periodo_3, periodo_4, antiguo]
                        numbers_vencido = [periodo_1, periodo_2, periodo_3, periodo_4, antiguo]
                        
                        total = round(sum(numbers), 2)
                        total_vencido = round(sum(numbers_vencido), 2)
                        
                        total_actual += actual
                        total_periodo_1 += periodo_1
                        total_periodo_2 += periodo_2
                        total_periodo_3 += periodo_3
                        total_periodo_4 += periodo_4
                        total_antiguo += antiguo
                        valor_total_adeudado += total
                        valor_total_vencido += total_vencido
                                
                        summary_account_move_lines.append({
                            'cliente': partner,
                            'actual': round(actual, 2),
                            'periodo1': round(periodo_1, 2),
                            'periodo2': round(periodo_2, 2),
                            'periodo3': round(periodo_3, 2),
                            'periodo4': round(periodo_4, 2),
                            'antiguo': round(antiguo, 2),
                            'total_adeudado': round(total, 2),
                            'total_vencido': round(total_vencido, 2),
                        })
                        
                    domain.remove(('partner_id', '=', result.get('partner_id', None)))
                    
                summary_account_move_lines.append({
                    'cliente': 'Total vencido por cobrar',
                    'actual': round(total_actual, 2),
                    'periodo1': round(total_periodo_1, 2),
                    'periodo2': round(total_periodo_2, 2),
                    'periodo3': round(total_periodo_3, 2),
                    'periodo4': round(total_periodo_4, 2),
                    'antiguo': round(total_antiguo, 2),
                    'total_adeudado': round(valor_total_adeudado, 2),
                    'total_vencido': round(valor_total_vencido, 2),
                })

                return summary_account_move_lines
                
        if move_lines:
            actual = 0
            periodo_1 = 0
            periodo_2 = 0
            periodo_3 = 0
            periodo_4 = 0
            antiguo = 0
            
            partner = self.env['res.partner'].browse(client_id).name
            
            for line in move_lines:
                fecha_vencida = line.move_id.invoice_date_due
                
                court_date_date = datetime.strptime(court_date, '%Y-%m-%d')
                
                dias_transcurridos = (court_date_date.date() - fecha_vencida).days
                
                # dias_transcurridos = (fecha_actual.date() - fecha_vencida).days
                
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
            
            numbers = [actual, periodo_1, periodo_2, periodo_3, periodo_4, antiguo]
            numbers_vencido = [periodo_1, periodo_2, periodo_3, periodo_4, antiguo]
            
            total = round(sum(numbers), 2)
            total_vencido = round(sum(numbers_vencido), 2)
                    
            summary_account_move_lines.append({
                'cliente': partner,
                'actual': round(actual, 2),
                'periodo1': round(periodo_1, 2),
                'periodo2': round(periodo_2, 2),
                'periodo3': round(periodo_3, 2),
                'periodo4': round(periodo_4, 2),
                'antiguo': round(antiguo, 2),
                'total_adeudado': round(total, 2),
                'total_vencido': round(total_vencido, 2),
            })

            return summary_account_move_lines
        
        else:
            raise ValidationError("¡No se encontraron registros para los criterios dados!")
    