from odoo import http
from odoo.exceptions import AccessError, MissingError
from odoo.addons.account.controllers.portal import PortalAccount
from odoo.http import request
import base64
import json
from werkzeug.utils import redirect


import logging
_logger = logging.getLogger(__name__)

class CustomPortalEcAccountEdi(PortalAccount):
    
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'refund_count' in counters:
            values['refund_count'] = request.env['account.move'].search_count(self._get_out_refund_domain()) \
                if request.env['account.move'].check_access_rights('read', raise_exception=False) else 0

        return values
    
    def _get_out_refund_domain(self):
        return [('state', 'not in', ('cancel', 'draft')), ('move_type', '=', 'out_refund')]
    
    @http.route(['/my/credit-notes', '/my/credit-notes/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_credit_notes(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        data = {
            'status': 'success',
            'message': 'Este es un mensaje en JSON',
            'page': page,
        }
        return request.make_response(json.dumps(data), headers={'Content-Type': 'application/json'})

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

        # Genera los valores para la vista y renderiza la página
        values = self._invoice_get_page_view_values(invoice_sudo, access_token, **kw)
        #return request.render("ec_account_edi_extend.portal_invoice_form")
        
        # Usar sudo para permitir acceso al backend
        invoice_sudo = invoice_sudo.sudo()
    
        # Redirigir al backend: vista formulario de account.move
        backend_url = f'/web#model=account.move&id={invoice_sudo.id}&action={invoice_sudo.env.ref("account.action_move_out_invoice_type").id}&view_type=form'
        return redirect(backend_url)
