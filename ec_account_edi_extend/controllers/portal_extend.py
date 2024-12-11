from odoo import http
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request
import base64


import logging
_logger = logging.getLogger(__name__)

class CustomPortalEcAccountEdi(CustomerPortal):
    
    # def _prepare_home_portal_values(self, counters):
    #     values = super()._prepare_home_portal_values(counters)
    #     if 'refund_count' in counters:
    #         refund_count = request.env['account.move'].search_count(self._get_out_refund_domain()) \
    #             if request.env['account.move'].check_access_rights('read', raise_exception=False) else 0
    #         values['refund_count'] = refund_count
    #     return values
    
    # def _get_invoices_domain(self):
    #     return [('state', 'not in', ('cancel', 'draft')), ('move_type', 'in', ('out_refund'))]
    
    # @http.rout(['/my/credit-notes', '/my/credit-notes/page/<int:page>'], type='http', auth="user", website=True)
    # def portal_my_credit_notes(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
    #     pass

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
        return request.render("account.portal_invoice_page", values)
