/** @odoo-module */

import publicWidget from 'web.public.widget';
import "portal.portal";

publicWidget.registry.PortalHomeCounters.include({
    /**
     * @override
     */
    _getCountersAlwaysDisplayed() {
        return this._super(...arguments).concat([
            'refund_count',
            'withholding_count',
            'remission_count',
            'retention_count',
            'debit_note_count',
        ]);
    },
});
