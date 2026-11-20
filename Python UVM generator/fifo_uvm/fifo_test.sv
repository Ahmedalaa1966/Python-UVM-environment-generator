`include "uvm_macros.svh"

class fifo_test extends uvm_test;

    `uvm_component_utils(fifo_test)

    fifo_env      envh;
    fifo_sequence seqh;

    function new(string name = "fifo_test", uvm_component parent = null);
        super.new(name, parent);
    endfunction : new

    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        envh = fifo_env     ::type_id::create("envh", this);         // create the env
        seqh = fifo_sequence::type_id::create("seqh");               // create the sequence (object, so no parent)
    endfunction : build_phase

    virtual task run_phase(uvm_phase phase);
        phase.raise_objection(this);
        phase.phase_done.set_drain_time(this, 100ns);              // let the last items reach the monitor/scoreboard
        seqh.start(envh.agenth.sqrh);                              // run the sequence on the agent's sequencer
        phase.drop_objection(this);
    endtask : run_phase

endclass : fifo_test
