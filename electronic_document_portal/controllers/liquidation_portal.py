# PORTAL LIQUIDACIONES DE COMPRAS

from odoo import http, _
from odoo.osv import expression
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.account.controllers.portal import PortalAccount
from odoo.http import request

import logging
_logger = logging.getLogger(__name__)

class LiquidationPortalController(PortalAccount):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'liquidation_count' in counters:
            values['liquidation_count'] = request.env['account.move'].search_count(self._get_liquidation_domain()) \
                if request.env['account.move'].check_access_rights('read', raise_exception=False) else 0

        return values
    
    
    def _get_liquidation_domain(self):
        # Dominio para liquidaciones de compras (in_invoice)
        user = request.env.user
        printer_default_ids = user.printer_default_ids
        
        domain = [
            ('state', 'not in', ('canceled', 'draft')),
            ('move_type', '=', 'in_invoice'), 
            ('liquidation', '=', True)
        ]

        if user.has_group('base.group_portal'):
            domain.append(('state_sri', '=', 'authorized'))
        
        if printer_default_ids:
            domain.append(('journal_id.printer_id', 'in', printer_default_ids.ids))
        
        return domain
    

    def _prepare_my_liquidation_values(self, page, date_begin, date_end, sortby, filterby, domain=None, url="/my/liquidations"):
        values = self._prepare_portal_layout_values()
        
        Liquidation = request.env['account.move']

        domain = expression.AND([
            domain or [],
            self._get_liquidation_domain(),
        ])

        searchbar_sortings = self._get_account_searchbar_sortings()
        # default sort by order
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        values.update({
            'date': date_begin,
            # content according to pager and archive selected
            # lambda function to get the liquidation recordset when the pager will be defined in the main method of a route
            'liquidations': lambda pager_offset: (
                Liquidation.search(domain, order=order, limit=self._items_per_page, offset=pager_offset)
                if Liquidation.check_access_rights('read', raise_exception=False) else
                Liquidation
            ),
            'page_name': 'liquidation',
            'pager': {  # vals to define the pager.
                "url": url,
                "url_args": {'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
                "total": Liquidation.search_count(domain) if Liquidation.check_access_rights('read', raise_exception=False) else 0,
                "page": page,
                "step": self._items_per_page,
            },
            'default_url': url,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        
        return values
    

    @http.route(['/my/liquidations', '/my/liquidations/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_liquidation(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        # Metodo que genera el contenido de retenciones
        values = self._prepare_my_liquidation_values(page, date_begin, date_end, sortby, filterby)

        # pager
        pager = portal_pager(**values['pager'])

        # content according to pager and archive selected
        liquidations = values['liquidations'](pager['offset'])
        request.session['my_liquidations_history'] = liquidations.ids[:100]

        values.update({
            'liquidations': liquidations,
            'pager': pager,
        })
        return request.render("electronic_document_portal.portal_my_liquidations", values)
    
