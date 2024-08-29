odoo.define('pos_customer_validated.customer_validation', (require) => {
    "use strict";

    const rpc = require('web.rpc')
    const PartnerListScreen = require('point_of_sale.PartnerListScreen')
    const Registries = require('point_of_sale.Registries');

    const PartnerListScreenExtend = PartnerListScreen => class extends PartnerListScreen {
        setup() {
            super.setup();
        }

        async saveChanges(event) {
            const partnerId = await this.rpc({
                model: "res.partner",
                method: "create_from_ui",
                args: [event.detail.processedChanges],
            });

            await this.env.pos._loadPartners([partnerId]);
            this.state.selectedPartner = this.env.pos.db.get_partner_by_id(partnerId);
            this.confirm();
        }
    }

    Registries.Component.extend(PartnerListScreen, PartnerListScreenExtend);

    return PartnerListScreen;

});
