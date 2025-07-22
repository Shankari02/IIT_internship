module transmission (
    input        i_Clock,        // 10 MHz clock
    input        i_Rx_Serial,    // UART RX
	 input        i_Enable,       // Reset gate pin
    output reg [7:0] i_Data_Out,   // I channel 8-bit DAC
    output reg [7:0] q_Data_Out,   // Q channel 8-bit DAC
    output reg       i_LED,       // Toggles on each byte
	 output reg       q_LED
);

  parameter CLKS_PER_BIT = 10;  // For 1Mbps baud with 50 MHz clock
  parameter HOLD_DELAY   = 1; // Hold delay to stabilize DAC

  reg [7:0]  r_Clock_Count = 0;
  reg [2:0]  r_Bit_Index   = 0;
  reg [7:0]  r_Rx_Byte     = 0;
  reg [2:0]  r_SM_Main     = 0;
  reg        r_Rx_Data_R   = 1'b1;
  reg        r_Rx_Data     = 1'b1;
  reg        r_IQ_toggle   = 0; // 0 = I, 1 = Q
  reg [15:0] r_Hold_Counter = 0;
  reg r_Enable_prev = 0;
  reg r_Receive_Enable = 0;  // Latch that holds whether receiving is enabled

  parameter s_IDLE         = 3'b000;
  parameter s_RX_START_BIT = 3'b001;
  parameter s_RX_DATA_BITS = 3'b010;
  parameter s_RX_STOP_BIT  = 3'b011;
  parameter s_HOLD         = 3'b100;

  // Metastability protection
  always @(posedge i_Clock) begin
    r_Rx_Data_R <= i_Rx_Serial;
    r_Rx_Data   <= r_Rx_Data_R;
  end

  // Toggle r_Receive_Enable on rising edge of i_Enable
  always @(posedge i_Clock) begin
  r_Enable_prev <= i_Enable;
  
	if (~r_Enable_prev && i_Enable) begin
		r_Receive_Enable <= ~r_Receive_Enable;  // Toggle on rising edge
	end
  end

  // UART FSM
  always @(posedge i_Clock) begin
    case (r_SM_Main)
		s_IDLE: begin
		r_Clock_Count <= 0;
		r_Bit_Index   <= 0;
		if (r_Receive_Enable && r_Rx_Data == 0)  // Check the toggle latch
			r_SM_Main <= s_RX_START_BIT;
		end

      s_RX_START_BIT: begin
        if (r_Clock_Count == 25) begin
          if (r_Rx_Data == 0) begin
            r_Clock_Count <= 0;
            r_SM_Main     <= s_RX_DATA_BITS;
          end else
            r_SM_Main <= s_IDLE;
        end else
          r_Clock_Count <= r_Clock_Count + 1;
      end

      s_RX_DATA_BITS: begin
        if (r_Clock_Count < 49) begin
          r_Clock_Count <= r_Clock_Count + 1;
        end else begin
          r_Clock_Count <= 0;
          r_Rx_Byte[r_Bit_Index] <= r_Rx_Data;
          if (r_Bit_Index < 7)
            r_Bit_Index <= r_Bit_Index + 1;
          else begin
            r_Bit_Index <= 0;
            r_SM_Main   <= s_RX_STOP_BIT;
          end
        end
      end

      s_RX_STOP_BIT: begin
        if (r_Clock_Count < 49)
          r_Clock_Count <= r_Clock_Count + 1;
        else begin
          r_Clock_Count <= 0;
          if (r_IQ_toggle == 0) begin
            i_Data_Out <= r_Rx_Byte;
				i_LED <= ~i_LED;
          end else begin
            q_Data_Out <= r_Rx_Byte;
				q_LED <= ~q_LED;
			end
          r_IQ_toggle <= ~r_IQ_toggle;
          r_Hold_Counter <= 0;
          r_SM_Main <= s_HOLD;
        end
      end

      s_HOLD: begin
        if (r_Hold_Counter < HOLD_DELAY)
          r_Hold_Counter <= r_Hold_Counter + 1;
        else
          r_SM_Main <= s_IDLE;
      end

      default: r_SM_Main <= s_IDLE;
    endcase
  end

endmodule
