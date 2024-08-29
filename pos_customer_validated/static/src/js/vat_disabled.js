odoo.define('pos_customer_validated.vat_disabled', (require) => {
    "use strict";

    const rpc = require('web.rpc')
    const PartnerDetailsEdit = require('point_of_sale.PartnerDetailsEdit')
    const Registries = require('point_of_sale.Registries');

    const PartnerDetailsEditExtend = PartnerDetailsEdit => class extends PartnerDetailsEdit {
        setup() {
            super.setup()

            const partner = this.props.partner;

            const vat = partner.vat

            if(vat) {
                const input_vat = document.querySelector('input[name="vat"]')

                if(input_vat) input_vat.disabled = true;
            }

        }
    }

    Registries.Component.extend(PartnerDetailsEdit, PartnerDetailsEditExtend);

    return PartnerDetailsEdit;

});