################################################################################################
## G U I A S  D E  R E M I S I O N #############################################################
################################################################################################

from odoo import http, _
from odoo.osv import expression
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from collections import OrderedDict
from odoo.http import request

class PortalShippingGuide(CustomerPortal):
    
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'shipping_guide_count' in counters:
            values['shipping_guide_count'] = 0

        return values