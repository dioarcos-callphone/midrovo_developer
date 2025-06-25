# PORTAL GUIAS DE REMISION
from odoo import http, _
from odoo.osv import expression
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from collections import OrderedDict
import base64

# import logging
# _logger = logging.getLogger(__name__)

class RemissionPortalController(CustomerPortal):
    
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'remission_count' in counters:
            values['remission_count'] = request.env['account.remision'].search_count(self._get_remission_domain()) \
                if request.env['account.remision'].check_access_rights('read', raise_exception=False) else 0

        return values
    

    def _get_remission_domain(self):
        # Dominio para guias de remision
        user = request.env.user
        printer_default_ids = user.printer_default_ids
        
        domain = [('state', 'not in', ('canceled', 'draft'))]

        if user.has_group('base.group_portal'):
            domain.append(('state_sri', '=', 'authorized'))
        
        if printer_default_ids:
            domain.append(('printer_id', 'in', printer_default_ids.ids))
        
        return domain
    
    def _remission_get_page_view_values(self, remission, access_token, **kwargs):
        values = {
            'page_name': 'remission',
            'remission': remission,
        }
        return self._get_page_view_values(remission, access_token, values, 'my_remissions_history', False, **kwargs)
    
    def _get_remission_searchbar_sortings(self):
        return {
            'date': {'label': _('Fecha'), 'order': 'delivery_date desc'},
            'name': {'label': _('Referencia'), 'order': 'document_number desc'},
            'state': {'label': _('Estado'), 'order': 'state'},
        }
    
    # metodo que genera el contenido de retenciones
    @http.route(['/my/remissions', '/my/remissions/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_remission(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_my_remission_values(page, date_begin, date_end, sortby, filterby)

        # pager
        pager = portal_pager(**values['pager'])

        # content according to pager and archive selected
        remissions = values['remissions'](pager['offset'])
        request.session['my_remissions_history'] = remissions.ids[:100]

        values.update({
            'remissions': remissions,
            'pager': pager,
        })
        return request.render("electronic_document_portal.portal_my_remissions", values)
    
    @http.route(['/my/remissions/<int:remission_id>'], type='http', auth="public", website=True)
    def portal_my_remission_detail(self, remission_id, access_token=None, report_type=None, download=False, **kw):
        try:
            # Verifica el acceso al documento
            remission_sudo = self._document_check_access('account.remision', remission_id, access_token)
            
        except (AccessError, MissingError):
            return request.redirect('/my')

        # Cambia el reporte referenciado
        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(
                model=remission_sudo,
                report_type=report_type,
                report_ref='ec_account_edi.e_delivery_note_qweb',  # Nuevo valor para report_ref
                download=download
            )
            
        if report_type == 'xml':
            xml_name = remission_sudo.xml_data_id.xml_name
            xml_bytes = remission_sudo.xml_authorized
            
            # Si el XML está en base64, lo decodificamos
            xml_decode = base64.b64decode(xml_bytes)
             
            filename = xml_name
            headers = [
                ('Content-Type', 'application/xml'),
                ('Content-Disposition', f'attachment; filename={filename}')
            ]
            
            return request.make_response(xml_decode, headers=headers)
        
        values = self._remission_get_page_view_values(remission_sudo, access_token, **kw)
        
        return request.render("electronic_document_portal.portal_remission_page", values)
    
    def _get_remission_searchbar_filters(self):
        return {
            'all': {
                'label': _('Todos'),
                'domain': []
            },
            'auth': {
                'label': _('Autorizados'),
                'domain': [
                    ('state_sri', '=', 'authorized'),
                ]
            },
            'reject': {
                'label': _('No Autorizados'), 
                'domain': [
                    ('state_sri', '!=', 'authorized')
                ]
            },
        }
    
    def _get_searchbar_inputs(self):
        return {
            'all': {'label': _('Todos'), 'input': 'all'},
            'partner': {'label': _('Cliente'), 'input': 'partner'},
            'name': {'label': _('Numero del documento'), 'input': 'name'},
        }
    
    def _get_search_domain(self, search_in, search):
            if search_in == 'partner':
                return [('partner_id.name', 'ilike', search)]
            elif search_in == 'name':
                return [('name', 'ilike', search)]
            elif search_in == 'all':
                return ['|', ('name', 'ilike', search), ('partner_id.name', 'ilike', search)]
            return []
    
    def _prepare_my_remission_values(self, page, date_begin, date_end, sortby, filterby, search=None, search_in='all', domain=None, url="/my/remissions"):
        values = self._prepare_portal_layout_values()
        
        Remission = request.env['account.remision']

        domain = expression.AND([
            domain or [],
            self._get_remission_domain(),
        ])

        searchbar_sortings = self._get_remission_searchbar_sortings()
        # default sort by order
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        searchbar_inputs = self._get_searchbar_inputs()

        if search and search_in:
            domain += self._get_search_domain(search_in, search)

        searchbar_filters = self._get_remission_searchbar_filters()
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        values.update({
            'date': date_begin,
            # content according to pager and archive selected
            # lambda function to get the shipping_guides recordset when the pager will be defined in the main method of a route
            'remissions': lambda pager_offset: (
                Remission.search(domain, order=order, limit=self._items_per_page, offset=pager_offset)
                if Remission.check_access_rights('read', raise_exception=False) else
                Remission
            ),
            'page_name': 'remission',
            'pager': {  # vals to define the pager.
                "url": url,
                "url_args": {'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
                "total": Remission.search_count(domain) if Remission.check_access_rights('read', raise_exception=False) else 0,
                "page": page,
                "step": self._items_per_page,
            },
            'default_url': url,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
            'searchbar_inputs': searchbar_inputs,
        })
        
        return values
    
    