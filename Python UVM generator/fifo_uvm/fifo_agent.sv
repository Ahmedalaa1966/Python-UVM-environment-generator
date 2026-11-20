`include "uvm_macros.svh"

class fifo_agent extends uvm_agent;

    `uvm_component_utils(fifo_agent)                                 // factory registration

    fifo_driver    drvh;                                             // driver handle
    fifo_monitor   monh;                                             // monitor handle
    fifo_sequencer sqrh;                                             // sequencer handle
    virtual fifo_if vif;                                             // virtual interface handle

    function new(string name = "fifo_agent", uvm_component parent = null);
        super.new(name, parent);
    endfunction : new

    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);

        // get the virtual interface from the top through the config db
        if (!uvm_config_db#(virtual fifo_if)::get(this, "", "vif", vif))
            `uvm_fatal("NO_VIF", "virtual interface not received")

        monh = fifo_monitor::type_id::create("monh", this);          // monitor always created

        if (get_is_active() == UVM_ACTIVE) begin                   // driver + sequencer only if active
            drvh = fifo_driver   ::type_id::create("drvh", this);
            sqrh = fifo_sequencer::type_id::create("sqrh", this);
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

endclass : fifo_agent
