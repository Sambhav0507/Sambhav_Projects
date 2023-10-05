library ieee, std;
use ieee.std_logic_1164.all;
use ieee.std_logic_textio.all;
use std.textio.all;

entity ASCII_Read_test is
end entity;

architecture reader of ASCII_Read_test is
	component CHORDEncoder
	    port(clk, rst: in std_logic;
	    a: in std_logic_vector(7 downto 0);
	    data_valid: out std_logic;
	    z: out std_logic_vector(7 downto 0));
	end component;
	signal input_sig, output_sig: std_logic_vector (7 downto 0);
	signal clk, rst: std_logic;
	signal flag:std_logic:='0';
begin
	dut_instance: CHORDEncoder
		port map ( clk => clk, rst => rst,a => input_sig, data_valid => flag,z => output_sig);
	
	process
		file input_file: text open read_mode is "test.txt";
		file output_file: text open write_mode is "out.txt";
		variable input_line, output_line: line;
		variable input_var, output_var : std_logic_vector (7 downto 0);	
    	variable it:integer:=0;
	begin
		clk <= '1';
			wait for 1 ns;
			clk <= '0';
			wait for 1 ns;
		while not endfile(input_file) loop
			readline (input_file, input_line);
			read (input_line, input_var);
			input_sig <= input_var;
			wait for 1 ns;
			clk <= '1';
			wait for 1 ns;
			clk <= '0';
			wait for 1 ns;
      
        	if flag='1' then
				output_var := output_sig;
				write (output_line, output_var);
				writeline (output_file, output_line);
        	end if;
			wait for 1 ns;
    	end loop;
    
    

    while it<10 loop
        input_sig<="00000000";
        wait for 1 ns;
			clk <= '1';
			wait for 1 ns;
			clk <= '0';
			wait for 1 ns;
        if flag='1' then
			output_var := output_sig;
			write (output_line, output_var);
			writeline (output_file, output_line);
        end if;
			wait for 1 ns;
			it:=it+1;
    end loop;
      
    wait;
	end process;

end architecture;