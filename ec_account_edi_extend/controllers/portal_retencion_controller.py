################################################################################################
## R E T E N C I O N E S #######################################################################
################################################################################################

from odoo import http, _
from odoo.osv import expression
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from collections import OrderedDict
from odoo.http import request
import base64


import logging
_logger = logging.getLogger(__name__)

class PortalWithholding(CustomerPortal):
    
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'withholding_count' in counters:
            values['withholding_count'] = request.env['account.withhold'].search_count(self._get_withholdings_domain()) \
                if request.env['account.withhold'].check_access_rights('read', raise_exception=False) else 0
                
        return values
    
    # domain para documentos de retencion
    def _get_withholdings_domain(self):
        return [('state', 'not in', ('canceled', 'draft'))]
    
    def _withholding_get_page_view_values(self, withholding, access_token, **kwargs):
        values = {
            'page_name': 'withholding',
            'withholding': withholding,
        }
        return self._get_page_view_values(withholding, access_token, values, 'my_withholdings_history', False, **kwargs)
    
    def _get_withholding_searchbar_sortings(self):
        return {
            'date': {'label': _('Fecha'), 'order': 'creation_date desc'},
            'name': {'label': _('Referencia'), 'order': 'l10n_latam_document_number desc'},
            'state': {'label': _('Estado'), 'order': 'state'},
        }
    
    # metodo que genera el contenido de retenciones
    @http.route(['/my/withholding', '/my/withholding/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_withholding(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_my_withholding_values(page, date_begin, date_end, sortby, filterby)
        
        _logger.info(f'MOSTRANDO VALORES >>> { values }')

        # pager
        pager = portal_pager(**values['pager'])

        # content according to pager and archive selected
        withholdings = values['withholdings'](pager['offset'])
        request.session['my_withholdings_history'] = withholdings.ids[:100]

        values.update({
            'withholdings': withholdings,
            'pager': pager,
        })
        return request.render("ec_account_edi_extend.portal_my_withholdings", values)
    
    @http.route(['/my/withholdings/<int:withholding_id>'], type='http', auth="public", website=True)
    def portal_my_withholding_detail(self, withholding_id, access_token=None, report_type=None, download=False, **kw):
        try:
            # Verifica el acceso al documento
            withhold_sudo = self._document_check_access('account.withhold', withholding_id, access_token)
            
        except (AccessError, MissingError):
            return request.redirect('/my')

        # Cambia el reporte referenciado
        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(
                model=withhold_sudo,
                report_type=report_type,
                report_ref='ec_account_edi.e_retention_qweb',  # Nuevo valor para report_ref
                download=download
            )
            
        if report_type == 'xml':
            xml_name = withhold_sudo.xml_name
            xml_bytes = withhold_sudo.xml_report
            
            # Si el XML está en base64, lo decodificamos
            xml_decode = base64.b64decode(xml_bytes)
             
            filename = xml_name
            headers = [
                ('Content-Type', 'application/xml'),
                ('Content-Disposition', f'attachment; filename={filename}')
            ]
            
            return request.make_response(xml_decode, headers=headers)
    
    def _prepare_my_withholding_values(self, page, date_begin, date_end, sortby, filterby, domain=None, url="/my/withholdings"):
        values = self._prepare_portal_layout_values()
        
        AccountWithhold = request.env['account.withhold']

        domain = expression.AND([
            domain or [],
            self._get_withholdings_domain(),
        ])

        searchbar_sortings = self._get_withholding_searchbar_sortings()
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
            'withholdings': lambda pager_offset: (
                AccountWithhold.search(domain, order=order, limit=self._items_per_page, offset=pager_offset)
                if AccountWithhold.check_access_rights('read', raise_exception=False) else
                AccountWithhold
            ),
            'page_name': 'withholding',
            'pager': {  # vals to define the pager.
                "url": url,
                "url_args": {'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
                "total": AccountWithhold.search_count(domain) if AccountWithhold.check_access_rights('read', raise_exception=False) else 0,
                "page": page,
                "step": self._items_per_page,
            },
            'default_url': url,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        
        return values
    
    
