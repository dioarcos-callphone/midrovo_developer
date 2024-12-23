################################################################################################
## G U I A S  D E  R E M I S I O N #############################################################
################################################################################################

from odoo import http, _
from odoo.osv import expression
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
import base64

class PortalShippingGuide(CustomerPortal):
    
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'shipping_guide_count' in counters:
            values['shipping_guide_count'] = request.env['account.remision'].search_count(self._get_shipping_guide_domain()) \
                if request.env['account.remision'].check_access_rights('read', raise_exception=False) else 0

        return values
    
    # domain para documentos de guias de remision
    def _get_shipping_guide_domain(self):
        # Se obtiene el punto de emisión del usuario interno actual
        user = request.env.user
        printer_default_ids = user.printer_default_ids
        
        domain = [('state', 'not in', ('canceled', 'draft'))]
        
        if printer_default_ids:
            domain.append(('printer_id', '=', printer_default_ids.ids))
        
        return domain
    
    def _shipping_guide_get_page_view_values(self, shipping_guide, access_token, **kwargs):
        values = {
            'page_name': 'shipping_guide',
            'shipping_guide': shipping_guide,
        }
        return self._get_page_view_values(shipping_guide, access_token, values, 'my_shipping_guides_history', False, **kwargs)
    
    def _get_shipping_guide_searchbar_sortings(self):
        return {
            'date': {'label': _('Fecha'), 'order': 'delivery_date desc'},
            'name': {'label': _('Referencia'), 'order': 'document_number desc'},
            'state': {'label': _('Estado'), 'order': 'state'},
        }
    
    # metodo que genera el contenido de retenciones
    @http.route(['/my/shipping_guide', '/my/shipping_guide/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_shipping_guide(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_my_shipping_guide_values(page, date_begin, date_end, sortby, filterby)

        # pager
        pager = portal_pager(**values['pager'])

        # content according to pager and archive selected
        shipping_guides = values['shipping_guides'](pager['offset'])
        request.session['my_shipping_guides_history'] = shipping_guides.ids[:100]

        values.update({
            'shipping_guides': shipping_guides,
            'pager': pager,
        })
        return request.render("ec_account_edi_extend.portal_my_shipping_guides", values)
    
    @http.route(['/my/shipping_guides/<int:shipping_guide_id>'], type='http', auth="public", website=True)
    def portal_my_shipping_guide_detail(self, shipping_guide_id, access_token=None, report_type=None, download=False, **kw):
        try:
            # Verifica el acceso al documento
            shipping_guide_sudo = self._document_check_access('account.remision', shipping_guide_id, access_token)
            
        except (AccessError, MissingError):
            return request.redirect('/my')

        # Cambia el reporte referenciado
        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(
                model=shipping_guide_sudo,
                report_type=report_type,
                report_ref='ec_account_edi.e_delivery_note_qweb',  # Nuevo valor para report_ref
                download=download
            )
            
        if report_type == 'xml':
            xml_name = shipping_guide_sudo.xml_data_id.xml_name
            xml_bytes = shipping_guide_sudo.xml_report
            
            # Si el XML está en base64, lo decodificamos
            xml_decode = base64.b64decode(xml_bytes)
             
            filename = xml_name
            headers = [
                ('Content-Type', 'application/xml'),
                ('Content-Disposition', f'attachment; filename={filename}')
            ]
            
            return request.make_response(xml_decode, headers=headers)
    
    def _prepare_my_shipping_guide_values(self, page, date_begin, date_end, sortby, filterby, domain=None, url="/my/shipping_guides"):
        values = self._prepare_portal_layout_values()
        
        AccountShippingGuide = request.env['account.remision']

        domain = expression.AND([
            domain or [],
            self._get_shipping_guide_domain(),
        ])

        searchbar_sortings = self._get_shipping_guide_searchbar_sortings()
        # default sort by order
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        values.update({
            'date': date_begin,
            # content according to pager and archive selected
            # lambda function to get the shipping_guides recordset when the pager will be defined in the main method of a route
            'shipping_guides': lambda pager_offset: (
                AccountShippingGuide.search(domain, order=order, limit=self._items_per_page, offset=pager_offset)
                if AccountShippingGuide.check_access_rights('read', raise_exception=False) else
                AccountShippingGuide
            ),
            'page_name': 'shipping_guide',
            'pager': {  # vals to define the pager.
                "url": url,
                "url_args": {'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
                "total": AccountShippingGuide.search_count(domain) if AccountShippingGuide.check_access_rights('read', raise_exception=False) else 0,
                "page": page,
                "step": self._items_per_page,
            },
            'default_url': url,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        
        return values
    
    