`include "uvm_macros.svh"

class fifo_env extends uvm_env;

    `uvm_component_utils(fifo_env)

    fifo_agent      agenth;
    fifo_scoreboard scbh;
    fifo_coverage   covh;

    function new(string name = "fifo_env", uvm_component parent = null);
        super.new(name, parent);
    endfunction : new

    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        agenth = fifo_agent     ::type_id::create("agenth", this);   // agent
        scbh   = fifo_scoreboard::type_id::create("scbh",   this);   // scoreboard
        covh   = fifo_coverage  ::type_id::create("covh",   this);   // coverage collector
        `uvm_info(get_type_name(), "fifo Environment build phase", UVM_LOW)
    endfunction : build_phase

    virtual function void connect_phase(uvm_phase phase);
        super.connect_phase(phase);
        agenth.monh.mon_ap.connect(scbh.analysis_export);          // monitor -> scoreboard
        agenth.monh.mon_ap.connect(covh.analysis_export);          // monitor -> coverage
    endfunction : connect_phase

endclass : fifo_env
