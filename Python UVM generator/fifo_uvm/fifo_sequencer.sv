`include "uvm_macros.svh"

class fifo_sequencer extends uvm_sequencer #(fifo_sequence_item);

    `uvm_component_utils(fifo_sequencer)                             // registration in the UVM factory

    function new(string name = "fifo_sequencer", uvm_component parent = null);
        super.new(name, parent);
    endfunction : new

endclass : fifo_sequencer
