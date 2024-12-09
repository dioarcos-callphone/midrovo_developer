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
                
                # if detail.move_id.move_type == 'entry':
                #     _logger.info('ENTRAAAA')
                #     entry += amount_residual
                
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
                
                court_date_date = datetime.strptime(court_date, '%Y-%m-%d')
                
                dias_transcurridos = (court_date_date.date() - date_due).days
                
                # _logger.info(f'DIAS TRANSCURRIDOS >>> { dias_transcurridos }')
                # _logger.info(f'MONTO RESIDUAL >>> { amount_residual }')

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
            #     total = total - entry
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
                'total_adeudado': total,
                'total_vencido': total_vencido,
                'lines': account_move_lines_filtered
            }
            
            return {
                'doc_ids': docids,
                'doc_model': 'report.account_due.report_account_due',
                'data': data,
                'is_summary': is_summary,
                'options': accounts_receivable_data,
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
                    partner_id = group['partner_id'][0]  # ID del cliente
                    processed_results.append({
                        'partner_id': partner_id,
                        'amount_residual': group['amount_residual'],
                        'partner_id_count': group['partner_id_count'],
                    })
                    
                for result in processed_results:
                    domain.append(('partner_id', '=', result.get('partner_id')))
                    
                    partner = self.env['res.partner'].browse(client_id).name
                    
                    move_lines = move_lines.search(move_lines)
                    
                    if move_lines:
                        actual = 0
                        periodo_1 = 0
                        periodo_2 = 0
                        periodo_3 = 0
                        periodo_4 = 0
                        antiguo = 0
                        
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
                            'actual': actual,
                            'periodo1': periodo_1,
                            'periodo2': periodo_2,
                            'periodo3': periodo_3,
                            'periodo4': periodo_4,
                            'antiguo': antiguo,
                            'total_adeudado': total,
                            'total_vencido': total_vencido
                        })

                        return summary_account_move_lines               
                                  
                
        # summary_account_move_lines = []
                
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
                'actual': actual,
                'periodo1': periodo_1,
                'periodo2': periodo_2,
                'periodo3': periodo_3,
                'periodo4': periodo_4,
                'antiguo': antiguo,
                'total_adeudado': total,
                'total_vencido': total_vencido
            })

            return summary_account_move_lines
        
        else:
            raise ValidationError("¡No se encontraron registros para los criterios dados!")
    