// decryptor.v
module decryptor #(
    parameter N = 3233,        // RSA modulus
    parameter d = 2753         // RSA private key (calculated: 17 * 2753 ≡ 1 mod 3120)
)(
    input  wire         clk,
    input  wire         reset,
    input  wire [15:0]  encrypted_char, 
    output reg  [7:0]   decrypted_char 
);

    // General RSA decryption using modular exponentiation
    // This implementation can decrypt any message encrypted with the same RSA keys
    // Formula: plaintext = ciphertext^d mod N
    
    // Internal registers for the iterative modular exponentiation algorithm
    reg [31:0] base;           // Base value (ciphertext)
    reg [31:0] result;         // Accumulating result
    reg [15:0] exponent;       // Current exponent value
    reg [4:0]  bit_count;      // Counter for exponent bits
    reg        computing;      // Flag indicating computation in progress
    reg [15:0] input_buffer;   // Buffer to store input during computation
    
    // Next-state combinatorial logic
    reg [31:0] next_base;
    reg [31:0] next_result;
    reg [15:0] next_exponent;
    reg [4:0]  next_bit_count;
    reg        next_computing;
    reg [15:0] next_input_buffer;
    reg [7:0]  next_decrypted_char;
    
    // Combinatorial logic block
    always @(*) begin
        // Default: hold current values
        next_base = base;
        next_result = result;
        next_exponent = exponent;
        next_bit_count = bit_count;
        next_computing = computing;
        next_input_buffer = input_buffer;
        next_decrypted_char = decrypted_char;
        
        if (!computing) begin
            // Start new computation when input changes
            if (encrypted_char != input_buffer) begin
                next_input_buffer = encrypted_char;
                next_base = encrypted_char;
                next_result = 32'd1;
                next_exponent = d;
                next_bit_count = 5'd12;  // Number of bits needed for d=2753
                next_computing = 1'b1;
            end
        end else begin
            // Perform one iteration of square-and-multiply algorithm
            if (bit_count > 0) begin
                // If current bit of exponent is 1, multiply result by base
                if (exponent[0]) begin
                    next_result = (result * base) % N;
                end
                // Square the base and shift exponent right
                next_base = (base * base) % N;
                next_exponent = exponent >> 1;
                next_bit_count = bit_count - 1;
            end else begin
                // Computation complete
                next_decrypted_char = result[7:0];  // Extract ASCII character
                next_computing = 1'b0;
            end
        end
    end
    
    // Sequential logic block
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            decrypted_char <= 8'b0;
            base <= 32'b0;
            result <= 32'b0;
            exponent <= 16'b0;
            bit_count <= 5'b0;
            computing <= 1'b0;
            input_buffer <= 16'b0;
        end else begin
            // Update all registers with next-state values
            decrypted_char <= next_decrypted_char;
            base <= next_base;
            result <= next_result;
            exponent <= next_exponent;
            bit_count <= next_bit_count;
            computing <= next_computing;
            input_buffer <= next_input_buffer;
        end
    end

endmodule