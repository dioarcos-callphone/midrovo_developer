# PORTAL RETENCIONES
from odoo import http, _
from odoo.osv import expression
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
import base64

# import logging
# _logger = logging.getLogger(__name__)

class RetentionPortalController(CustomerPortal):
    
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'retention_count' in counters:
            values['retention_count'] = request.env['account.withhold'].search_count(self._get_retention_domain()) \
                if request.env['account.withhold'].check_access_rights('read', raise_exception=False) else 0
                
        return values
    
    
    def _get_retention_domain(self):
        # Domain para documentos de retencion
        user = request.env.user
        printer_default_ids = user.printer_default_ids
        
        domain = [('state', 'not in', ('canceled', 'draft'))]

        if user.has_group('base.group_portal'):
            domain.append(('state_sri', '=', 'authorized'))
        
        if printer_default_ids:
            domain.append(('printer_id', 'in', printer_default_ids.ids))
        
        return domain
    
    def _retention_get_page_view_values(self, retention, access_token, **kwargs):
        values = {
            'page_name': 'retention',
            'retention': retention,
        }
        return self._get_page_view_values(retention, access_token, values, 'my_retentions_history', False, **kwargs)
    
    def _get_retention_searchbar_sortings(self):
        return {
            'date': {'label': _('Fecha'), 'order': 'creation_date desc'},
            'name': {'label': _('Referencia'), 'order': 'l10n_latam_document_number desc'},
            'state': {'label': _('Estado'), 'order': 'state'},
        }
    
    
    @http.route(['/my/retentions', '/my/retentions/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_retention(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        # Metodo que genera el contenido de retenciones
        values = self._prepare_my_retention_values(page, date_begin, date_end, sortby, filterby)

        # pager
        pager = portal_pager(**values['pager'])

        # content according to pager and archive selected
        retentions = values['retentions'](pager['offset'])
        request.session['my_retentions_history'] = retentions.ids[:100]

        values.update({
            'retentions': retentions,
            'pager': pager,
        })
        return request.render("electronic_document_portal.portal_my_retentions", values)
    
    @http.route(['/my/retentions/<int:retention_id>'], type='http', auth="public", website=True)
    def portal_my_retention_detail(self, retention_id, access_token=None, report_type=None, download=False, **kw):
        try:
            # Verifica el acceso al documento
            retention_sudo = self._document_check_access('account.withhold', retention_id, access_token)
            
        except (AccessError, MissingError):
            return request.redirect('/my')

        # Cambia el reporte referenciado
        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(
                model=retention_sudo,
                report_type=report_type,
                report_ref='ec_account_edi.e_retention_qweb',  # Nuevo valor para report_ref
                download=download
            )
            
        if report_type == 'xml':
            xml_name = retention_sudo.xml_name
            xml_bytes = retention_sudo.xml_report
            
            # Si el XML está en base64, lo decodificamos
            xml_decode = base64.b64decode(xml_bytes)
             
            filename = xml_name
            headers = [
                ('Content-Type', 'application/xml'),
                ('Content-Disposition', f'attachment; filename={filename}')
            ]
            
            return request.make_response(xml_decode, headers=headers)
        
        values = self._retention_get_page_view_values(retention_sudo, access_token, **kw)

        currency = request.env.company.currency_id
        values["display_currency"] = currency
        
        return request.render("electronic_document_portal.portal_retention_page", values)
    
    
    def _prepare_my_retention_values(self, page, date_begin, date_end, sortby, filterby, domain=None, url="/my/retentions"):
        values = self._prepare_portal_layout_values()
        
        Retention = request.env['account.withhold']

        domain = expression.AND([
            domain or [],
            self._get_retention_domain(),
        ])

        searchbar_sortings = self._get_retention_searchbar_sortings()
        # default sort by order
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        values.update({
            'date': date_begin,
            # content according to pager and archive selected
            # lambda function to get the withholdings recordset when the pager will be defined in the main method of a route
            'retentions': lambda pager_offset: (
                Retention.search(domain, order=order, limit=self._items_per_page, offset=pager_offset)
                if Retention.check_access_rights('read', raise_exception=False) else
                Retention
            ),
            'page_name': 'retention',
            'pager': {  # vals to define the pager.
                "url": url,
                "url_args": {'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
                "total": Retention.search_count(domain) if Retention.check_access_rights('read', raise_exception=False) else 0,
                "page": page,
                "step": self._items_per_page,
            },
            'default_url': url,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        
        return values
    
    
