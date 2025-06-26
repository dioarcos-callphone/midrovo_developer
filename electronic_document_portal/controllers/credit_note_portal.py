# PORTAL NOTAS DE CREDITO

from odoo import http, _
from odoo.osv import expression
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.account.controllers.portal import PortalAccount
from odoo.http import request
from collections import OrderedDict

# import logging
# _logger = logging.getLogger(__name__)

class CreditNotePortalController(PortalAccount):

    def _prepare_home_portal_values(self, counters):
        # Extendemos este metodo que calcula la cantidad de registros filtrados por un dominio
        values = super()._prepare_home_portal_values(counters)
        if 'refund_count' in counters:
            values['refund_count'] = request.env['account.move'].search_count(self._get_out_refund_domain()) \
                if request.env['account.move'].check_access_rights('read', raise_exception=False) else 0

        return values

    
    def _get_out_refund_domain(self):
        # Dominio para las notas de credito (out_refund)
        user = request.env.user
        printer_default_ids = user.printer_default_ids
        
        domain = [
            ('state', 'not in', ('cancel', 'draft')),
            ('move_type', '=', 'out_refund')
        ]

        if user.has_group('base.group_portal'):
            domain.append(('state_sri', '=', 'authorized'))
        
        if printer_default_ids:
            domain.append(('printer_id', 'in', printer_default_ids.ids))
        
        return domain
    
    def _get_credit_note_searchbar_filters(self):
        return {
            'all': {
                'label': _('Todos'),
                'domain': []
            },
            'auth': {
                'label': _('Autorizados'),
                'domain': [
                    ('move_type', '=', 'out_refund'),
                    ('state_sri', '=', 'authorized'),
                ]
            },
            'reject': {
                'label': _('No Autorizados'), 
                'domain': [
                    ('move_type', '=', 'out_refund'),
                    ('state_sri', '!=', 'authorized')
                ]
            },
        }
    

    def _prepare_my_refunds_values(self, page, date_begin, date_end, sortby, filterby, search=None, search_in='name', domain=None, url="/my/refunds"):
        values = self._prepare_portal_layout_values()
        CreditNote = request.env['account.move']

        domain = expression.AND([
            domain or [],
            self._get_out_refund_domain(),
        ])

        searchbar_sortings = self._get_account_searchbar_sortings()
        # default sort by order
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        searchbar_inputs = self._get_searchbar_inputs()

        if search and search_in:
            domain += self._get_search_domain(search_in, search)

        searchbar_filters = self._get_credit_note_searchbar_filters()
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
                CreditNote.search(domain, order=order, limit=self._items_per_page, offset=pager_offset)
                if CreditNote.check_access_rights('read', raise_exception=False) else
                CreditNote
            ),
            'page_name': 'refund',
            'pager': {  # vals to define the pager.
                "url": url,
                "url_args": {'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
                "total": CreditNote.search_count(domain) if CreditNote.check_access_rights('read', raise_exception=False) else 0,
                "page": page,
                "step": self._items_per_page,
            },
            'default_url': url,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
            'searchbar_inputs': searchbar_inputs,
            'search_in': search_in,
        })
        
        return values
    

    # metodo que genera el contenido de notas de credito
    @http.route(['/my/refunds', '/my/refunds/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_refund(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, search=None, search_in='name', **kw):
        values = self._prepare_my_refunds_values(page, date_begin, date_end, sortby, filterby, search, search_in)

        # pager
        pager = portal_pager(**values['pager'])

        # content according to pager and archive selected
        refunds = values['refunds'](pager['offset'])
        request.session['my_refunds_history'] = refunds.ids[:100]

        values.update({
            'refunds': refunds,
            'pager': pager,
        })
        return request.render("electronic_document_portal.portal_my_refunds", values)

    