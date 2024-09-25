/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
import { rpc } from '@web';
export class SaleListController extends ListController {
   setup() {
       super.setup();
   }
   async actionPDF() {
       // Hacer una llamada RPC al método 'action_pdf' en el modelo 'product.product'
       const { data } = await rpc({
           model: 'product.product',
           method: 'action_pdf',
       });

   }
}
registry.category("views").add("button_in_tree", {
   ...listView,
   Controller: SaleListController,
   buttonTemplate: "button_sale.ListView.Buttons",
});