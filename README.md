# FOUNDRY

### **A Lightweight Manufacturing Execution System (MES) & BOM Manager.**

> **⚠️ STATUS: PRE-ALPHA / WORK IN PROGRESS**
> **THIS SYSTEM IS CURRENTLY IN ACTIVE DEVELOPMENT AND IS NOT YET READY FOR PRODUCTION USE.**
> Features may break, schemas may migrate, and logic is subject to change. This is a "build in public" project—**contributions, bug reports, and pull requests are highly appreciated.**

---

**FOUNDRY** is a local, browser-based ecosystem designed for managing Bills of Materials, visual production routing, inventory logic, and financial analytics for small-scale manufacturing and prototyping.

It operates on a **"Zero-Cloud" philosophy**—all data resides locally in a portable SQLite database. You own the infrastructure.

---

## CORE MODULES

### 1. FOUNDRY_VAULT (`index.html`)

**The central repository for project data and component specifications.**

* **BOM Management:** Create projects and define parts with bulk costs, quantities, and lead times.
* **Cost Analysis:** Real-time calculation of Design Valuation based on component requirements.
* **Schema Resilience:** Automatic database repair and column migration on load.

### 2. FOUNDRY_PRODUCTION (`production.html`)

**A node-based visual router for defining manufacturing logic.**

* **Visual Flow:** Drag-and-drop interface for connecting parts to manufacturing processes (CNC, 3D Printing, Assembly).
* **Smart Wiring:** Enforced **1-to-1 output logic** to ensure strict process linearity.
* **Inventory Awareness:** Real-time enforcement of BOM limits. You cannot place more parts on the router than exist in the Vault design.
* **Auto-Cleanup:** Smart port consolidation automatically removes gaps when nodes or wires are deleted.

### 3. FOUNDRY_COMMAND (`command.html`)

**The executive dashboard for operations, logistics, and intelligence.**

* **Financials:** Tracks Gross Revenue, Procurement Burn, and Net Profit.
* **Inventory Runway:** Auto-calculates how many units can be built based on the "weakest link" component stock.
* **Logistics Pipeline:** Separate workflows for "Production Work Orders" and "Shipping Fulfillment."
* **Revenue Logging:** Instant recognition of revenue upon sale registration, with decoupled inventory deduction.

---

## TECHNICAL ARCHITECTURE

* **Backend:** Python (Flask). Acts purely as a file server and binary blob persistence layer.
* **Database:** SQLite (via `sql.js`). The database engine runs entirely in the browser (WASM). The backend only saves the binary file to disk.
* **Frontend:** Vanilla JS + Tailwind CSS. No build steps required.
* **Persistence:** Data is saved to `projects_vault.db` in the root directory.

---

## INSTALLATION & SETUP

FOUNDRY runs on a lightweight Python backend.

### Prerequisites

* Python 3.x
* Pip

### 1. Install Dependencies

```bash
pip install flask flask_cors

```

### 2. Launch the Engine

Run the application server. This will create the `projects_vault.db` file automatically if it does not exist.

```bash
python app.py

```

### 3. Access the System

Open your browser and navigate to:
`http://localhost:8000`

---

## OPERATIONAL WORKFLOW

1. **Design (Vault):** Create a Project. Add Parts (Screws, PCBs, Motors). Define their cost and bulk purchase quantities.
2. **Procure (Command):** Go to the Command tab. Click "Restock" on parts to simulate buying inventory. This increases your "Burn" metric.
3. **Route (Production):** Open Manufacturing Ops. Drag parts onto the canvas. Connect them through Process nodes (e.g., *Part -> Assembly -> Final*). Save the flow.
4. **Sell (Command):** Register a Sale.
* *If Finished Stock exists:* The system logs revenue and prepares a Shipping Ticket.
* *If Stock is 0:* The system creates a Work Order.


5. **Build (Command):** Click "Finalize Build" on a Work Order. This deducts raw components from the Vault and increments Finished Goods inventory.
6. **Ship (Command - Logistics):** Authorize the shipment to close the ticket and deduct the Finished Good from inventory.

---

*Licensed under the FOUNDRY SOURCE LICENSE (FSL). See `LICENSE` for details.*
