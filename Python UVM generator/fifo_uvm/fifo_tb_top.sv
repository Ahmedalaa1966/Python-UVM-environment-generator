`timescale 1ns/1ps

module tb_top;

    import uvm_pkg::*;
    `include "uvm_macros.svh"
    import fifo_tb_pkg::*;

    // ---------------------------------------------------
    // Clock
    // ---------------------------------------------------
    logic clk = 1'b0;
    always #5 clk = ~clk;                 // 10 ns period

    // ---------------------------------------------------
    // Interface
    // ---------------------------------------------------
    fifo_if fifo_vif (clk);

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
        uvm_config_db#(virtual fifo_if)::set(null, "*", "vif", fifo_vif);
        run_test("fifo_test");            // +UVM_TESTNAME on the command line overrides this
    end

endmodule : tb_top
