### **Core Systems, Entities, and Concepts**

*   **OPUS**: The core business system used for managing bookings and agency commissions.
*   **Vessel Voyage Direction (VVD)**: A unique identifier for a vessel's specific journey, combining the vessel code, voyage number, and direction (e.g., E for East, W for West). It is fundamental for tracking, scheduling, and financial assignment.
*   **Commission Vessel Voyage Direction (Comm.VVD)**: The specific vessel (trunk, pre, or post) to which commissions are calculated and distributed.
*   **Revenue Vessel Voyage Direction (R.VVD)**: A representative vessel, created monthly with the format `CNTR+YYMM`, for the purpose of assigning costs and revenues.
*   **Trunk Vessel (T/VVD)**: The main, ocean-crossing vessel in a voyage, as distinct from pre-carriage or on-carriage feeder vessels.
*   **Service Lane**: A defined, scheduled trade route (e.g., `ACE` for SWACO-2) operated by vessels.
*   **Service Scope**: A grouping of origin and destination regions (e.g., `TA` for TRANS ATLANTIC TRADE) that defines a trade area. It is often appended with a directional indicator:
    *   **(EB)**: Eastbound
    *   **(WB)**: Westbound
    *   **(NB)**: Northbound
    *   **(SB)**: Southbound
*   **Yard Code**: A unique identifier for a specific terminal or container yard, typically structured as `[CountryCode][LocationCode][NumericID]` (e.g., `AEJEA01` for DP WORLD JEBEL ALI - TERMINAL 1).
*   **Local Control Centre (LCC)**: A geographical or business classification for managing container inventory and operations.
*   **House Bill of Lading (HBL)**: A B/L created by an Ocean Transport Intermediary (OTI) like a freight forwarder or NVOCC, as distinct from the master B/L issued by the carrier.
*   **Restricted Usage Label (RU Label)**: A system for tagging equipment to manage its use for specific purposes, such as `FLOW`, `One-Way Free Use (OW FU)`, `OFFHIRE`, `DOMESTIC`, `SALE`, `Garment on Hanger (GOH)`, and `REEFER`.

### **Booking Process and Statuses**

*   **Standby Booking**: A booking status subject to validation against constraints. Final statuses include `Firm`, `Stand By` (waiting), `Cancel`, or `Error`.
*   **Master Constraint Table (MCT)**: A core system component for the automated validation of bookings against operational and commercial constraints.
*   **Sequential Validation (Seq. Val. Stage)**: A progressive validation logic where Standby checks constraints in a specific order (e.g., `CMD` -> `EQR` -> `EQA`) and stops at the first failure.
*   **Guidance Codes (GD1-GD6, XXX)**: System-generated actions based on MCT rules for handling a booking.
    *   **GD1**: OK to Book.
    *   **GD2**: Book to next available vessel.
    *   **GD3**: Escalate to Reefer/Booking role.
    *   **GD4**: Auto-escalate to Customer Service (CSVC).
    *   **GD5**: Auto-escalate to Regional/Global HQ.
    *   **GD6**: Decline.
    *   **XXX**: No valid constraints found.
*   **Booking Roll Over (R/O)**: The operational process of moving a container that was not loaded on its intended voyage to a subsequent voyage.
*   **Bill of Lading Data Release (BDR)**: A key milestone indicating the completion of all export-side documentation processes, signifying a handover of responsibility to the import-side team.
*   **Receive Channel**: The specific platform or method through which a booking is received, such as `CargoSmart (CSM)`, `INTTRA (INT)`, `DAKOSY (DAK)`, or `WEB (QTE)` for bookings originating from a web quotation.
*   **Also Notify Party**: A secondary party, in addition to the primary Notify Party, that must be informed of the cargo's arrival.

### **Cargo and Container Types**

*   **Cargo Type (Codes)**:
    *   **F**: Full cargo.
    *   **P**: Positioning empty container (an empty container moved for operational reasons).
    *   **R**: Revenue empty container (an empty container transported for a fee).
*   **Awkward Cargo (A/K, AK)**: Containerized or non-containerized cargo with irregular dimensions requiring special handling and planning.
*   **Break Bulk (B/B, BB)**: Non-containerized cargo that is too large or heavy for even specialized containers (like Open Tops or Flat Racks) and requires individual handling.
*   **Garment on Hanger (GOH)**: A specialized service for shipping clothing on hangers within containers fitted with racks and bars.
*   **Shipper's Own Container (S.O.C.)**: A flag indicating the container is provided by the shipper, not the carrier.
*   **Reefer Twenty-foot Equivalent Unit (RTEU)**: A specific unit of measurement for a 20-foot reefer container.
*   **Reefer Forty-foot Equivalent Unit (RFEU)**: A specific unit of measurement for a 40-foot reefer container.

### **Financial and Commission Terminology**

*   **Agency Commission Management (ACM)**: A specific module within the OPUS system for managing agent commissions.
*   **Consultation Slip Receipt (CSR)**: A key document/process created for a group of audited commission records to authorize payment processing in the financial system (SAP/ERP).
*   **Forwarding Agency Commission (FAC)**: A specific commission type and system module primarily used for European outbound cargo.
*   **Freight Forwarder Compensation (FFC)**: A specific commission type and system module primarily for US and Canadian outbound cargo.
*   **Cross Booking Commission**: Commission paid when the booking office is different from the loading office.
*   **Brokerage of South West Asia (SWA BRKG)**: A specific commission paid to agents acting as freight forwarders in the SWA region, in addition to general commission.
*   **Container Handling Fee (CHF)**: A fixed fee per container paid to an agent for arranging equipment for cargo.
*   **Container Sales Fee (CSF)**: An additional fee to the CHF to reward sales activity.
*   **Reefer Container Sales Fee (RCSF)**: A further incentive paid for running (operating) reefer containers, which generate higher revenue.
*   **Sail Arrival Date (S/A Date)**: A rule-based date (using ETA or ETD of the Commission VVD at specific points like POL or POD) that determines the validity period of a commission agreement.
*   **Transport Expense (TRS)**: A specific deduction from the base revenue, comprising inland haulage and feederage charges, used during commission calculation.
*   **Third Party Billing (TPB)**: Refers to cost recovery from vendors. A TPB Customer Code is created to invoice a service provider.

### **Operational Codes and Statuses**

*   **Container Movement Status Codes**: Standardized codes representing the current state of a container in its lifecycle.
    *   **OC (Outbound Full CY - Gate In)**: A full container has been received at the origin container yard.
    *   **VL (Vessel Loading)**: The container is being loaded onto the vessel.
    *   **TS (Transhipment)**: The container is in the process of being moved from one vessel to another.
    *   **IC (Inbound Full CY - Gate In)**: A full container has arrived at the destination container yard.
    *   **ID (Inbound Full Delivery - Gate Out)**: A full container has left the destination yard for final delivery.
    *   **MT (Empty - Gate In)**: An empty container has been returned to the yard.
    *   **OP (Empty Release to Shipper - Gate Out)**: An empty container has been released to the shipper for loading.
    *   **DOMESTIC Codes (CD, CE, CI, CO, CP, CT)**: A parallel set of movement statuses used specifically for North America Domestic business.
*   **Automated Manifest System (AMS) Filer**: A code indicating who files the customs manifest for a House B/L (1=Carrier, 2=NVOCC).
*   **Freight Retain Onboard (FROB)**: A customs status for cargo that remains on a vessel at a US port but is not discharged, as its final destination is outside the US.
*   **Entry Summary Declaration (ENS)**: The specific name for the 24-hour advanced manifest required for cargo entering the EU.
*   **Amendment Transmit Type (AI Type)**: Codes for manifest amendments, such as `ADD` (additional B/Ls), `UPDATE` (amendment), and `CANCEL` (deletion).