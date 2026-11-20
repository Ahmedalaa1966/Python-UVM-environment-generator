interface fifo_if (input logic clk);

    // declare your signals here

    // DUT view: it reads the inputs and drives the result
    modport dut (
    );

endinterface : fifo_if
