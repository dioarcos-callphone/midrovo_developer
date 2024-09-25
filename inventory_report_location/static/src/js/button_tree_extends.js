/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
export class SaleListController extends ListController {
   setup() {
       super.setup();
   }
   async actionPDF() {
       // Obtener los IDs de los productos seleccionados
       const selectedIds = this.selectedRecordIds;

       if (selectedIds.length === 0) {
           this._notify("No se han seleccionado productos", { type: "warning" });
           return;
       }

       // Hacer una llamada RPC al método 'action_pdf' en el modelo 'product.product'
       const { data } = await this._rpc({
           model: 'product.product',
           method: 'action_pdf',
           args: [selectedIds],
       });

   }
}
registry.category("views").add("button_in_tree", {
   ...listView,
   Controller: SaleListController,
   buttonTemplate: "button_sale.ListView.Buttons",
});