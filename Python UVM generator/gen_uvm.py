# gen_uvm.py
# Asks for the project name and generates a UVM environment skeleton.
# Every "@@" inside the templates is replaced by the project name.

import os

# ---------------------------------------------------------------
# Templates
# ---------------------------------------------------------------

seq_item = """`include "uvm_macros.svh"

class @@_sequence_item extends uvm_sequence_item;

    `uvm_object_utils(@@_sequence_item)                    // registration to the UVM factory

    // add your fields here

    function new(string name = "@@_sequence_item");
        super.new(name);
    endfunction : new

    virtual function string convert2string();
        return "";
    endfunction : convert2string

endclass : @@_sequence_item
"""

sequence = """`include "uvm_macros.svh"

class @@_sequence extends uvm_sequence #(@@_sequence_item);

    `uvm_object_utils(@@_sequence)                                 // registration in the UVM factory

    function new(string name = "@@_sequence");                     // constructor
        super.new(name);
    endfunction : new

    virtual task body();
        @@_sequence_item trn;                                      // handle for the sequence item
        `uvm_info(get_type_name(), "starting the uvm sequence", UVM_LOW)

        repeat (10) begin
            trn = @@_sequence_item::type_id::create("trn");        // create the transaction
            start_item(trn);                                       // blocks until the sequencer grants access
            if (!trn.randomize())                                  // randomize the transaction's fields
                `uvm_error(get_type_name(), "randomization failed")
            finish_item(trn);                                      // blocks until the driver finishes the item
            `uvm_info(get_type_name(),
                      $sformatf("generated transaction %s", trn.convert2string()),
                      UVM_LOW)
        end
    endtask : body

endclass : @@_sequence
"""

sequencer = """`include "uvm_macros.svh"

class @@_sequencer extends uvm_sequencer #(@@_sequence_item);

    `uvm_component_utils(@@_sequencer)                             // registration in the UVM factory

    function new(string name = "@@_sequencer", uvm_component parent = null);
        super.new(name, parent);
    endfunction : new

endclass : @@_sequencer
"""

driver = """`include "uvm_macros.svh"

class @@_driver extends uvm_driver #(@@_sequence_item);

    `uvm_component_utils(@@_driver)

    virtual @@_if vif;      // assigned by the agent in connect_phase

    function new(string name = "@@_driver", uvm_component parent = null);
        super.new(name, parent);
    endfunction : new

    virtual function void end_of_elaboration_phase(uvm_phase phase);
        super.end_of_elaboration_phase(phase);
        if (vif == null)
            `uvm_fatal("NO_VIF", "virtual interface not assigned to driver")
    endfunction : end_of_elaboration_phase

    virtual task run_phase(uvm_phase phase);
        @@_sequence_item trn;
        forever begin
            seq_item_port.get_next_item(trn);
            // drive the interface signals here
            seq_item_port.item_done();
        end
    endtask : run_phase

endclass : @@_driver
"""

monitor = """`include "uvm_macros.svh"

class @@_monitor extends uvm_monitor;

    `uvm_component_utils(@@_monitor)

    virtual @@_if vif;                                      // assigned by the agent in connect_phase
    uvm_analysis_port #(@@_sequence_item) mon_ap;           // broadcasts observed transactions

    function new(string name = "@@_monitor", uvm_component parent = null);
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
        @@_sequence_item trn;

        forever begin
            // sample the interface, fill trn, then broadcast it:
            // mon_ap.write(trn);
            @(posedge vif.clk);
        end
    endtask : run_phase

endclass : @@_monitor
"""

coverage = """`include "uvm_macros.svh"

class @@_coverage extends uvm_component;

    `uvm_component_utils(@@_coverage)

    uvm_analysis_export   #(@@_sequence_item) analysis_export;
    uvm_tlm_analysis_fifo #(@@_sequence_item) fifo;
    @@_sequence_item trn;

    covergroup @@_cg;
        // add your coverpoints here (they can use trn)
    endgroup : @@_cg

    function new(string name = "@@_coverage", uvm_component parent = null);
        super.new(name, parent);
        @@_cg = new();
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
            @@_cg.sample();
        end
    endtask : run_phase

endclass : @@_coverage
"""

scoreboard = """`include "uvm_macros.svh"

class @@_scoreboard extends uvm_scoreboard;

    `uvm_component_utils(@@_scoreboard)

    uvm_analysis_export   #(@@_sequence_item) analysis_export;
    uvm_tlm_analysis_fifo #(@@_sequence_item) fifo;

    int error_count;
    int pass_count;

    function new(string name = "@@_scoreboard", uvm_component parent = null);
        super.new(name, parent);
        error_count = 0;
        pass_count  = 0;
    endfunction : new

    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        analysis_export = new("analysis_export", this);
        fifo            = new("fifo", this);
        `uvm_info(get_type_name(), "@@ scoreboard build phase", UVM_LOW)
    endfunction : build_phase

    virtual function void connect_phase(uvm_phase phase);
        super.connect_phase(phase);
        analysis_export.connect(fifo.analysis_export);
    endfunction : connect_phase

    virtual task run_phase(uvm_phase phase);
        @@_sequence_item trn;
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

endclass : @@_scoreboard
"""

agent = """`include "uvm_macros.svh"

class @@_agent extends uvm_agent;

    `uvm_component_utils(@@_agent)                                 // factory registration

    @@_driver    drvh;                                             // driver handle
    @@_monitor   monh;                                             // monitor handle
    @@_sequencer sqrh;                                             // sequencer handle
    virtual @@_if vif;                                             // virtual interface handle

    function new(string name = "@@_agent", uvm_component parent = null);
        super.new(name, parent);
    endfunction : new

    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);

        // get the virtual interface from the top through the config db
        if (!uvm_config_db#(virtual @@_if)::get(this, "", "vif", vif))
            `uvm_fatal("NO_VIF", "virtual interface not received")

        monh = @@_monitor::type_id::create("monh", this);          // monitor always created

        if (get_is_active() == UVM_ACTIVE) begin                   // driver + sequencer only if active
            drvh = @@_driver   ::type_id::create("drvh", this);
            sqrh = @@_sequencer::type_id::create("sqrh", this);
        end
    endfunction : build_phase

    virtual function void connect_phase(uvm_phase phase);
        super.connect_phase(phase);

        monh.vif = vif;                                            // pass vif to the monitor

        if (get_is_active() == UVM_ACTIVE) begin
            drvh.seq_item_port.connect(sqrh.seq_item_export);      // driver <-> sequencer TLM connection
            drvh.vif = vif;                                        // pass vif to the driver
        end
    endfunction : connect_phase

endclass : @@_agent
"""

env = """`include "uvm_macros.svh"

class @@_env extends uvm_env;

    `uvm_component_utils(@@_env)

    @@_agent      agenth;
    @@_scoreboard scbh;
    @@_coverage   covh;

    function new(string name = "@@_env", uvm_component parent = null);
        super.new(name, parent);
    endfunction : new

    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        agenth = @@_agent     ::type_id::create("agenth", this);   // agent
        scbh   = @@_scoreboard::type_id::create("scbh",   this);   // scoreboard
        covh   = @@_coverage  ::type_id::create("covh",   this);   // coverage collector
        `uvm_info(get_type_name(), "@@ Environment build phase", UVM_LOW)
    endfunction : build_phase

    virtual function void connect_phase(uvm_phase phase);
        super.connect_phase(phase);
        agenth.monh.mon_ap.connect(scbh.analysis_export);          // monitor -> scoreboard
        agenth.monh.mon_ap.connect(covh.analysis_export);          // monitor -> coverage
    endfunction : connect_phase

endclass : @@_env
"""

test = """`include "uvm_macros.svh"

class @@_test extends uvm_test;

    `uvm_component_utils(@@_test)

    @@_env      envh;
    @@_sequence seqh;

    function new(string name = "@@_test", uvm_component parent = null);
        super.new(name, parent);
    endfunction : new

    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        envh = @@_env     ::type_id::create("envh", this);         // create the env
        seqh = @@_sequence::type_id::create("seqh");               // create the sequence (object, so no parent)
    endfunction : build_phase

    virtual task run_phase(uvm_phase phase);
        phase.raise_objection(this);
        phase.phase_done.set_drain_time(this, 100ns);              // let the last items reach the monitor/scoreboard
        seqh.start(envh.agenth.sqrh);                              // run the sequence on the agent's sequencer
        phase.drop_objection(this);
    endtask : run_phase

endclass : @@_test
"""

interface = """interface @@_if (input logic clk);

    // declare your signals here

    // DUT view: it reads the inputs and drives the result
    modport dut (
    );

endinterface : @@_if
"""

package = """package @@_tb_pkg;

    import uvm_pkg::*;
    `include "uvm_macros.svh"
    `include "@@_seq_item.sv"
    `include "@@_sequence.sv"
    `include "@@_sequencer.sv"
    `include "@@_driver.sv"
    `include "@@_monitor.sv"
    `include "@@_coverage.sv"
    `include "@@_scoreboard.sv"
    `include "@@_agent.sv"
    `include "@@_env.sv"
    `include "@@_test.sv"

endpackage : @@_tb_pkg
"""

tb_top = """`timescale 1ns/1ps

module tb_top;

    import uvm_pkg::*;
    `include "uvm_macros.svh"
    import @@_tb_pkg::*;

    // ---------------------------------------------------
    // Clock
    // ---------------------------------------------------
    logic clk = 1'b0;
    always #5 clk = ~clk;                 // 10 ns period

    // ---------------------------------------------------
    // Interface
    // ---------------------------------------------------
    @@_if @@_vif (clk);

    // ---------------------------------------------------
    // DUT
    // ---------------------------------------------------


    // ---------------------------------------------------
    // Reset (active high)
    // ---------------------------------------------------

    // ---------------------------------------------------
    // UVM start
    // ---------------------------------------------------
    initial begin
        uvm_config_db#(virtual @@_if)::set(null, "*", "vif", @@_vif);
        run_test("@@_test");            // +UVM_TESTNAME on the command line overrides this
    end

endmodule : tb_top
"""

# ---------------------------------------------------------------
# file name -> content
# ---------------------------------------------------------------

files = {
    "@@_seq_item.sv":   seq_item,
    "@@_sequence.sv":   sequence,
    "@@_sequencer.sv":  sequencer,
    "@@_driver.sv":     driver,
    "@@_monitor.sv":    monitor,
    "@@_coverage.sv":   coverage,
    "@@_scoreboard.sv": scoreboard,
    "@@_agent.sv":      agent,
    "@@_env.sv":        env,
    "@@_test.sv":       test,
    "@@_if.sv":         interface,
    "@@_pkg.sv":        package,
    "@@_tb_top.sv":     tb_top,
}

# ---------------------------------------------------------------
# Main
# ---------------------------------------------------------------

name = input("Enter the project name: ").strip()

if name == "":
    print("Project name cannot be empty.")
else:
    folder = name + "_uvm"
    if not os.path.exists(folder):
        os.makedirs(folder)

    for file_name in files:
        out_name = file_name.replace("@@", name)
        out_text = files[file_name].replace("@@", name)
        f = open(os.path.join(folder, out_name), "w")
        f.write(out_text)
        f.close()
        print("created " + folder + "/" + out_name)

    print("Done. Files are in the folder: " + folder)