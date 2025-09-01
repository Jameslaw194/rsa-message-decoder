// tb_decryptor.v
`timescale 1ns/1ps

module tb_decryptor;

    parameter MESSAGE_LENGTH = 20;

    // Clock and reset
    reg clk;
    reg reset;
    
    // Signals 
    reg [15:0] encrypted_char;
    reg [15:0] encrypted_message [0:MESSAGE_LENGTH-1];     
    wire [7:0] decrypted_char;
    
    integer i;

    // Instantiate the decryptor
    decryptor dut (
        .clk(clk),
        .reset(reset),
        .encrypted_char(encrypted_char),
        .decrypted_char(decrypted_char)
    );
    
    // Clock generation
    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end
    
    // Test sequence
    initial begin
        reset = 1;
        encrypted_char = 0;
        
        // Load encrypted message 
        $readmemh("data/message.hex", encrypted_message);
        
        // Come out of reset
        #10;
        reset = 0;

        // Decrypt message
        $display("Decrypting RSA message...");
        $display("Message:");
        for (i = 0; i < MESSAGE_LENGTH; i = i + 1) begin
            encrypted_char = encrypted_message[i];
            // The decryptor needs multiple clock cycles for each character
            repeat(15) @(posedge clk);
            $write("%c", decrypted_char);
        end

        // End simulation
        #10;
        $write("\n");
        $finish;
    end
endmodule