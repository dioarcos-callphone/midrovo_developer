odoo.define("credit_card_pos.ChromeExtend", (require) => {
    "use strict";
    const Registries = require("point_of_sale.Registries");
    const Chrome = require("point_of_sale.Chrome");

    const ChromeExtend = (Chrome) =>
        class extends Chrome {
            setup() {
                super.setup();
                console.log('ENTRANDO EN CHROME');
                console.log(this.env.pos.deactivate);
            }
        }

    Registries.Component.extend(Chrome, ChromeExtend);
});