`include "uvm_macros.svh"

class fifo_driver extends uvm_driver #(fifo_sequence_item);

    `uvm_component_utils(fifo_driver)

    virtual fifo_if vif;      // assigned by the agent in connect_phase

    function new(string name = "fifo_driver", uvm_component parent = null);
        super.new(name, parent);
    endfunction : new

    virtual function void end_of_elaboration_phase(uvm_phase phase);
        super.end_of_elaboration_phase(phase);
        if (vif == null)
            `uvm_fatal("NO_VIF", "virtual interface not assigned to driver")
    endfunction : end_of_elaboration_phase

    virtual task run_phase(uvm_phase phase);
        fifo_sequence_item trn;
        forever begin
            seq_item_port.get_next_item(trn);
            // drive the interface signals here
            seq_item_port.item_done();
        end
    endtask : run_phase

endclass : fifo_driver
