from odoo import http
from odoo.osv import expression
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.account.controllers.portal import PortalAccount
from odoo.http import request
from collections import OrderedDict
import base64

import logging
_logger = logging.getLogger(__name__)

class CustomPortalEcAccountEdi(PortalAccount):
    
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'refund_count' in counters:
            values['refund_count'] = request.env['account.move'].search_count(self._get_out_refund_domain()) \
                if request.env['account.move'].check_access_rights('read', raise_exception=False) else 0

        return values
    
    # domain para documentos de reembolso
    def _get_out_refund_domain(self):
        return [('state', 'not in', ('cancel', 'draft')), ('move_type', '=', 'out_refund')]
    
    # domain para documentos de factura
    # def _get_invoices_domain(self):
    #     return [('state', 'not in', ('cancel', 'draft')), ('move_type', '=', 'out_invoice')]

    
    @http.route(['/my/refund', '/my/refund/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_refund(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_my_refunds_values(page, date_begin, date_end, sortby, filterby)

        # pager
        pager = portal_pager(**values['pager'])

        # content according to pager and archive selected
        refunds = values['refunds'](pager['offset'])
        request.session['my_refunds_history'] = refunds.ids[:100]

        values.update({
            'refunds': refunds,
            'pager': pager,
        })
        return request.render("ec_account_edi_extend.portal_my_refunds", values)
    
    def _prepare_my_refunds_values(self, page, date_begin, date_end, sortby, filterby, domain=None, url="/my/refunds"):
        values = self._prepare_portal_layout_values()
        
        _logger.info(f'MOSTRANDO SELF >>>> { self }')
        
        _logger.info(f'MOSTRANDO VALUES 1 >>>> { values }')
        
        AccountRefund = request.env['account.move']

        domain = expression.AND([
            domain or [],
            self._get_out_refund_domain(),
        ])

        searchbar_sortings = self._get_account_searchbar_sortings()
        # default sort by order
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        searchbar_filters = self._get_account_searchbar_filters()
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        values.update({
            'date': date_begin,
            # content according to pager and archive selected
            # lambda function to get the invoices recordset when the pager will be defined in the main method of a route
            'refunds': lambda pager_offset: (
                AccountRefund.search(domain, order=order, limit=self._items_per_page, offset=pager_offset)
                if AccountRefund.check_access_rights('read', raise_exception=False) else
                AccountRefund
            ),
            'page_name': 'refund',
            'pager': {  # vals to define the pager.
                "url": url,
                "url_args": {'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
                "total": AccountRefund.search_count(domain) if AccountRefund.check_access_rights('read', raise_exception=False) else 0,
                "page": page,
                "step": self._items_per_page,
            },
            'default_url': url,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
        })
        
        _logger.info(f'MOSTRANDO VALUES 2 >>>> { values }')
        
        return values

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
        
        return request.render("ec_account_edi_extend.portal_invoice_form")
