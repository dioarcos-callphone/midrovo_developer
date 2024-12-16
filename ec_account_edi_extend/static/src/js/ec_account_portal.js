/** @odoo-module */

import publicWidget from 'web.public.widget';
import "portal.portal";

publicWidget.registry.PortalHomeCounters.include({
    /**
     * @override
     */
    _getCountersAlwaysDisplayed() {
        return this._super(...arguments).concat(['refund_count', 'withholdings_count']);
    },
});
