odoo.define("credit_card_pos.ChromeExtend", (require) => {
    "use strict";

    const Chrome = require("point_of_sale.Chrome");
    const Registries = require("point_of_sale.Registries");

    const ChromeExtend = (Chrome) =>
        class extends Chrome {
            setup() {
                super.setup()
                console.log("ESTAMOS EN CHROME")
                console.log(this)
            }
        }

    Registries.Component.extend(Chrome, ChromeExtend);

});