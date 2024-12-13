// /** @odoo-module */
// import { ListController } from "@web/views/list/list_controller";
// import { registry } from '@web/core/registry';
// import { listView } from '@web/views/list/list_view';
// import rpc from "web.rpc";
// export class SaleListController extends ListController {
//     setup() {
//        super.setup();
//     }
    
//     async actionPDF() {
//         try {
//             const selectedRecords = this.state.selectedIds;

//             if (selectedRecords.length === 0) {
//                 // Manejo de caso donde no hay registros seleccionados
//                 console.warn("No hay registros seleccionados");
//                 return;
//             }
            
//             const recordIds = selectedRecords.map(record => record.id);

//             console.log("Resultado:", recordIds);

//         } catch (error) {
//             console.log(error);
//         }
//     }
// }

// registry.category("views").add("button_in_tree", {
//     ...listView,
//     Controller: SaleListController,
//     buttonTemplate: "button_sale.ListView.Buttons",
// });
