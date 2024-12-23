################################################################################################
## L I Q U I D A C I O N  D E  C O M P R A S ###################################################
################################################################################################

from odoo import http, _
from odoo.osv import expression
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
import base64

class PortalPurchaseSettlement(CustomerPortal):
    
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'purchase_settlement_count' in counters:
            values['purchase_settlement_count'] = 0

        return values
    
    # domain para documentos de liquidacion de compra
    def _get_purchase_settlement_domain(self):
        # Se obtiene el punto de emisión del usuario interno actual
        user = request.env.user
        printer_default_ids = user.printer_default_ids
        
        domain = [('state', 'not in', ('canceled', 'draft'))]
        
        if printer_default_ids:
            domain.append(('printer_id', '=', printer_default_ids.ids))
        
        return domain
    
    def _purchase_settlement_get_page_view_values(self, purchase_settlement, access_token, **kwargs):
        values = {
            'page_name': 'purchase_settlement',
            'purchase_settlement': purchase_settlement,
        }
        return self._get_page_view_values(purchase_settlement, access_token, values, 'my_purchase_settlements_history', False, **kwargs)
    
    def _get_purchase_settlement_searchbar_sortings(self):
        return {
            'date': {'label': _('Fecha'), 'order': 'creation_date desc'},
            'name': {'label': _('Referencia'), 'order': 'l10n_latam_document_number desc'},
            'state': {'label': _('Estado'), 'order': 'state'},
        }
    
    # metodo que genera el contenido de retenciones
    @http.route(['/my/purchase_settlement', '/my/purchase_settlement/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_purchase_settlement(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_my_purchase_settlement_values(page, date_begin, date_end, sortby, filterby)

        # pager
        pager = portal_pager(**values['pager'])

        # content according to pager and archive selected
        purchase_settlements = values['purchase_settlements'](pager['offset'])
        request.session['my_purchase_settlements_history'] = purchase_settlements.ids[:100]

        values.update({
            'purchase_settlements': purchase_settlements,
            'pager': pager,
        })
        return request.render("ec_account_edi_extend.portal_my_purchase_settlements", values)
    
    @http.route(['/my/purchase_settlements/<int:purchase_settlement_id>'], type='http', auth="public", website=True)
    def portal_my_purchase_settlement_detail(self, purchase_settlement_id, access_token=None, report_type=None, download=False, **kw):
        try:
            # Verifica el acceso al documento
            purchase_settlement_sudo = self._document_check_access('account.withhold', purchase_settlement_id, access_token)
            
        except (AccessError, MissingError):
            return request.redirect('/my')

        # Cambia el reporte referenciado
        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(
                model=purchase_settlement_sudo,
                report_type=report_type,
                report_ref='ec_account_edi.e_retention_qweb',  # Nuevo valor para report_ref
                download=download
            )
            
        if report_type == 'xml':
            xml_name = purchase_settlement_sudo.xml_name
            xml_bytes = purchase_settlement_sudo.xml_report
            
            # Si el XML está en base64, lo decodificamos
            xml_decode = base64.b64decode(xml_bytes)
             
            filename = xml_name
            headers = [
                ('Content-Type', 'application/xml'),
                ('Content-Disposition', f'attachment; filename={filename}')
            ]
            
            return request.make_response(xml_decode, headers=headers)
    
    def _prepare_my_purchase_settlement_values(self, page, date_begin, date_end, sortby, filterby, domain=None, url="/my/purchase_settlements"):
        values = self._prepare_portal_layout_values()
        
        AccountPurchaseSettlement = request.env['account.withhold']

        domain = expression.AND([
            domain or [],
            self._get_purchase_settlement_domain(),
        ])

        searchbar_sortings = self._get_purchase_settlement_searchbar_sortings()
        # default sort by order
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        values.update({
            'date': date_begin,
            # content according to pager and archive selected
            # lambda function to get the purchase_settlements recordset when the pager will be defined in the main method of a route
            'purchase_settlements': lambda pager_offset: (
                AccountPurchaseSettlement.search(domain, order=order, limit=self._items_per_page, offset=pager_offset)
                if AccountPurchaseSettlement.check_access_rights('read', raise_exception=False) else
                AccountPurchaseSettlement
            ),
            'page_name': 'purchase_settlement',
            'pager': {  # vals to define the pager.
                "url": url,
                "url_args": {'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
                "total": AccountPurchaseSettlement.search_count(domain) if AccountPurchaseSettlement.check_access_rights('read', raise_exception=False) else 0,
                "page": page,
                "step": self._items_per_page,
            },
            'default_url': url,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        
        return values
    
    