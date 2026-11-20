`include "uvm_macros.svh"

class fifo_sequence_item extends uvm_sequence_item;

    `uvm_object_utils(fifo_sequence_item)                    // registration to the UVM factory

    // add your fields here

    function new(string name = "fifo_sequence_item");
        super.new(name);
    endfunction : new

    virtual function string convert2string();
        return "";
    endfunction : convert2string

endclass : fifo_sequence_item
