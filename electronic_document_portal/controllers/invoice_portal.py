# PORTAL FACTURAS

from odoo import http, _
from odoo.exceptions import AccessError, MissingError
from odoo.addons.account.controllers.portal import PortalAccount
from odoo.http import request
import base64

# import logging
# _logger = logging.getLogger(__name__)

class InvoicePortalController(PortalAccount):

    def _get_invoices_domain(self):
        # Dominio para las facturas de cliente
        user = request.env.user
        # Obtenemos el punto de emisión del usuario interno actual
        printer_default_ids = user.printer_default_ids
        
        domain = [
            ('state', 'not in', ('cancel', 'draft')),
            ('move_type', '=', 'out_invoice'),
            ('debit_origin_id', '=', False),
            ('debit_note', '=', False)
        ]

        if user.has_group('base.group_portal'):
            domain.append(('state_sri', '=', 'authorized'))
        
        if printer_default_ids:
            domain.append(('printer_id', 'in', printer_default_ids.ids))
        
        return domain
    
    
    def _prepare_my_invoices_values(self, page, date_begin, date_end, sortby, filterby, domain=None, url="/my/invoices"):
        # Extendemos este metodo para ocultar el filtro del search menu
        # Llamamos al método original con super
        values = super()._prepare_my_invoices_values(page, date_begin, date_end, sortby, filterby, domain=domain, url=url)
        
        # Quitamos los elementos relacionados con `searchbar_filters` y `filterby`
        values.pop('searchbar_filters', None)  # Elimina si existe
        values.pop('filterby', None)  # Elimina si existe
        
        # Retornamos los valores modificados
        return values
    
    
    def _invoice_get_page_view_values(self, invoice, access_token, **kwargs):
        move_type = invoice.move_type
        debit_note = invoice.debit_note or invoice.debit_origin_id
        history = 'my_invoices_history'

        values = {
            'page_name': 'invoice',
            'invoice': invoice,
        }

        # Separamos las facturas - notas de credito - notas de debito - liquidaciones de compra
        # para no mostrar en una sola vista ya que todas pertenecen a account_move

        if debit_note and move_type == 'out_invoice':
            values['page_name'] = 'debit_note'
            history = 'my_debit_notes_history'
        elif move_type == 'out_refund':
            values['page_name'] = 'refund'
            history = 'my_refunds_history'
        elif move_type == 'in_invoice':
            values['page_name'] = 'liquidation'
        
        return self._get_page_view_values(invoice, access_token, values, history, False, **kwargs)
    

    @http.route(['/my/invoices/<int:invoice_id>'], type='http', auth="public", website=True)
    def portal_my_invoice_detail(self, invoice_id, access_token=None, report_type=None, download=False, **kw):
        try:
            # Verifica el acceso al documento
            invoice_sudo = self._document_check_access('account.move', invoice_id, access_token)
            
        except (AccessError, MissingError):
            return request.redirect('/my')

        # Cambia el reporte referenciado
        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(
                model=invoice_sudo,
                report_type=report_type,
                report_ref='ec_account_edi.e_invoice_qweb',  # Nuevo valor para report_ref
                download=download
            )
            
        if report_type == 'xml':
            xml_name = invoice_sudo.xml_name
            xml_bytes = invoice_sudo.xml_report
            
            # Si el XML está en base64, lo decodificamos
            xml_decode = base64.b64decode(xml_bytes)
             
            filename = xml_name
            headers = [
                ('Content-Type', 'application/xml'),
                ('Content-Disposition', f'attachment; filename={filename}')
            ]
            
            return request.make_response(xml_decode, headers=headers)
        
        values = self._invoice_get_page_view_values(invoice_sudo, access_token, **kw)
        
        return request.render("account.portal_invoice_page", values)
        
