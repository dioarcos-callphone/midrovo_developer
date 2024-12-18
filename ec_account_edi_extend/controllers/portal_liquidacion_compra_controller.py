################################################################################################
## L I Q U I D A C I O N  D E  C O M P R A S ###################################################
################################################################################################

from odoo import http, _
from odoo.osv import expression
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from collections import OrderedDict
from odoo.http import request

class PortalPurchaseSettlement(CustomerPortal):
    
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'purchase_settlement_count' in counters:
            values['purchase_settlement_count'] = 0

        return values