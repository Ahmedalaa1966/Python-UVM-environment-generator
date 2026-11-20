`include "uvm_macros.svh"

class fifo_monitor extends uvm_monitor;

    `uvm_component_utils(fifo_monitor)

    virtual fifo_if vif;                                      // assigned by the agent in connect_phase
    uvm_analysis_port #(fifo_sequence_item) mon_ap;           // broadcasts observed transactions

    function new(string name = "fifo_monitor", uvm_component parent = null);
        super.new(name, parent);
    endfunction : new

    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        mon_ap = new("mon_ap", this);
    endfunction : build_phase

    virtual function void end_of_elaboration_phase(uvm_phase phase);
        super.end_of_elaboration_phase(phase);
        if (vif == null)
            `uvm_fatal("NO_VIF", "virtual interface not assigned to monitor")
    endfunction : end_of_elaboration_phase

    virtual task run_phase(uvm_phase phase);
        fifo_sequence_item trn;

        forever begin
            // sample the interface, fill trn, then broadcast it:
            // mon_ap.write(trn);
            @(posedge vif.clk);
        end
    endtask : run_phase

endclass : fifo_monitor
