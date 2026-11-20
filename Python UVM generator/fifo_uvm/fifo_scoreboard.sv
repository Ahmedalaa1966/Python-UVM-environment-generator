`include "uvm_macros.svh"

class fifo_scoreboard extends uvm_scoreboard;

    `uvm_component_utils(fifo_scoreboard)

    uvm_analysis_export   #(fifo_sequence_item) analysis_export;
    uvm_tlm_analysis_fifo #(fifo_sequence_item) fifo;

    int error_count;
    int pass_count;

    function new(string name = "fifo_scoreboard", uvm_component parent = null);
        super.new(name, parent);
        error_count = 0;
        pass_count  = 0;
    endfunction : new

    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        analysis_export = new("analysis_export", this);
        fifo            = new("fifo", this);
        `uvm_info(get_type_name(), "fifo scoreboard build phase", UVM_LOW)
    endfunction : build_phase

    virtual function void connect_phase(uvm_phase phase);
        super.connect_phase(phase);
        analysis_export.connect(fifo.analysis_export);
    endfunction : connect_phase

    virtual task run_phase(uvm_phase phase);
        fifo_sequence_item trn;
        forever begin
            fifo.get(trn);
            // compare against the reference model, then count:
            // pass_count++  or  error_count++
        end
    endtask : run_phase

    virtual function void report_phase(uvm_phase phase);
        super.report_phase(phase);
        `uvm_info("PASS_COUNT",  $sformatf("pass count  = %0d", pass_count),  UVM_LOW)
        `uvm_info("ERROR_COUNT", $sformatf("error count = %0d", error_count), UVM_LOW)
        if (error_count == 0) `uvm_info(get_type_name(), "TEST PASSED", UVM_NONE)
        else                  `uvm_info(get_type_name(), "TEST FAILED", UVM_NONE)
    endfunction : report_phase

endclass : fifo_scoreboard
