`include "uvm_macros.svh"

class fifo_coverage extends uvm_component;

    `uvm_component_utils(fifo_coverage)

    uvm_analysis_export   #(fifo_sequence_item) analysis_export;
    uvm_tlm_analysis_fifo #(fifo_sequence_item) fifo;
    fifo_sequence_item trn;

    covergroup fifo_cg;
        // add your coverpoints here (they can use trn)
    endgroup : fifo_cg

    function new(string name = "fifo_coverage", uvm_component parent = null);
        super.new(name, parent);
        fifo_cg = new();
    endfunction : new

    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        analysis_export = new("analysis_export", this);
        fifo            = new("fifo", this);
    endfunction : build_phase

    virtual function void connect_phase(uvm_phase phase);
        super.connect_phase(phase);
        analysis_export.connect(fifo.analysis_export);
    endfunction : connect_phase

    virtual task run_phase(uvm_phase phase);
        forever begin
            fifo.get(trn);
            fifo_cg.sample();
        end
    endtask : run_phase

endclass : fifo_coverage
