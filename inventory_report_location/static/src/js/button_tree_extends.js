/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
import rpc from "web.rpc";
export class SaleListController extends ListController {
    setup() {
       super.setup();
    }
    
    async actionPDF() {
        try {
            const result = await rpc.query({
                model: 'product.product',
                method: 'action_pdf',
            });

            if(result) {
                console.log('ENTRA AL RESULTADO')
                console.log(result)

                // const report = await rpc.query({
                //     model: 'report.inventory_report_location.report_stock_quantity',
                //     method: '_get_report_values'
                // })
            }

        } catch (error) {
            console.error("Error al generar el PDF:", error);
        }
    }
}

registry.category("views").add("button_in_tree", {
    ...listView,
    Controller: SaleListController,
    buttonTemplate: "button_sale.ListView.Buttons",
});
