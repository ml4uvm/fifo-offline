`timescale 1ns/1ps

module fifo_tb;

    parameter DATA_WIDTH = 8;
    parameter DEPTH = 8;

    logic clk;
    logic rst;

    logic write_en;
    logic read_en;
    logic [DATA_WIDTH-1:0] data_in;

    logic [DATA_WIDTH-1:0] data_out;
    logic full;
    logic empty;

    // DUT
    fifo #(
        .DATA_WIDTH(DATA_WIDTH),
        .DEPTH(DEPTH)
    ) dut (
        .clk(clk),
        .rst(rst),
        .write_en(write_en),
        .read_en(read_en),
        .data_in(data_in),
        .data_out(data_out),
        .full(full),
        .empty(empty)
    );

    // Clock generation
    always #5 clk = ~clk;

    // Stimulus
    initial begin
        $dumpfile("fifo.vcd");
        $dumpvars(0, fifo_tb);

        clk = 0;
        rst = 1;
        write_en = 0;
        read_en = 0;
        data_in = 0;

        // Reset
        #10;
        rst = 0;

        // --------------------
        // WRITE phase
        // --------------------
        repeat (5) begin
            @(posedge clk);
            write_en = 1;
            read_en = 0;
            data_in = $random;
        end

        @(posedge clk);
        write_en = 0;

        // --------------------
        // READ phase
        // --------------------
        repeat (5) begin
            @(posedge clk);
            read_en = 1;
            write_en = 0;
        end

        @(posedge clk);
        read_en = 0;

        // --------------------
        // SIMULTANEOUS RW
        // --------------------
        repeat (3) begin
            @(posedge clk);
            write_en = 1;
            read_en = 1;
            data_in = $random;
        end

        @(posedge clk);
        write_en = 0;
        read_en = 0;

        // --------------------
        // END
        // --------------------
        #20;
        $finish;
    end

endmodule