library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use ieee.numeric_std.all;

entity CHORDEncoder is
    port(clk, rst: in std_logic;
    a: in std_logic_vector(7 downto 0);
    data_valid: out std_logic;
    z: out std_logic_vector(7 downto 0));
end entity;

architecture behavior of CHORDEncoder is

    TYPE temp IS ARRAY (0 TO 31) OF STD_LOGIC_VECTOR (7 DOWNTO 0);


    function keyValue(vec: std_logic_vector(7 downto 0)) return integer is 
        begin
            if vec = "01000011" then
                return 1; --C
            elsif vec = "01100100" then
                return 2; --d
            elsif vec = "01000100" then
                return 3;  --D
            elsif vec = "01100101" then
                return 4; --e
            elsif vec = "01000101" then
                return 5; --E
            elsif vec = "01100110" then
                return 5; --f
            elsif vec = "01000110" then
                return 6; --F
            elsif vec = "01100111" then
                return 7; --g
            elsif vec = "01000111" then
                return 8; --G
            elsif vec = "01100001" then
                return 9; --a
            elsif vec = "01000001" then
                return 10; --A
            elsif vec = "01100010" then
                return 11; --b
            elsif vec = "01000010" then
                return 12; --B
            elsif vec = "01100011" then
                return 12; --c
            elsif vec = "00011111" then 
                return 13;
            else
                return 0;
            end if;
        end function;

    function replace_hash(vec : std_logic_vector(7 downto 0)) return std_logic_vector is
        variable replaced_vec : std_logic_vector(7 downto 0);
    begin
        if vec = "01000011" then
            replaced_vec := "01100100";
        elsif vec = "01000100" then
            replaced_vec := "01100101";
        elsif vec = "01000101" then
            replaced_vec := "01000110";
        elsif vec = "01000110" then
            replaced_vec := "01100111";
        elsif vec = "01000111" then
            replaced_vec := "01100001";
        elsif vec = "01000001" then
            replaced_vec := "01100010";
        elsif vec = "01000010" then
            replaced_vec := "01000011";
        end if;
    return replaced_vec;
    
    end function;

    begin
        process(clk, rst)
        variable buffer1: temp;
        variable buffer2: temp;
        variable head : integer := 0;
        variable tail : integer := 0;
        variable head2 : integer := 0;
        variable tail2 : integer := 0;
        begin
            
            if rising_edge(clk) then
                if keyValue(a) = 13 then
                        buffer1(tail-1) := replace_hash(buffer1(tail - 1));
                
                elsif keyValue(a) = 0 then 
                    if tail = head + 1 then
                        buffer2(tail2) := buffer1(head);
                        head := head + 1;
                        tail2 := tail2 + 1;
                        
                    elsif tail = head + 2 then
                        
                        buffer2(tail2) := buffer1(head);
                        head := head + 1;
                        tail2 := tail2 + 1;
                        buffer2(tail2) := buffer1(head);
                        head := head + 1;
                        tail2 := tail2 + 1;
                    
                    elsif tail = head + 3 then

                        if ((keyValue(buffer1(head + 1))- keyValue(buffer1(head))) mod 12) = 4 then
                            if ((keyValue(buffer1(head + 2))- keyValue(buffer1(head+1))) mod 12) = 3 then
                                buffer2(tail2) := buffer1(head);
                                tail2 := tail2 + 1;
                                buffer2(tail2):= "01001101";
                                tail2 := tail2 + 1;
                                head := head + 3;
                            else
                                buffer2(tail2) := buffer1(head);
                                tail2 := tail2 + 1;
                                head := head + 1;
                                buffer2(tail2) := buffer1(head);
                                head := head + 1;
                                tail2 := tail2 + 1;
                                buffer2(tail2) := buffer1(head);
                                head := head + 1;
                                tail2 := tail2 + 1;
                            end if;
                            
                        elsif ((keyValue(buffer1(head + 1))- keyValue(buffer1(head))) mod 12) = 3 then
                            if ((keyValue(buffer1(head + 2))- keyValue(buffer1(head + 1))) mod 12) = 4 then
                                buffer2(tail2) := buffer1(head);
                                tail2 := tail2 + 1;
                                buffer2(tail2) := "01101101";
                                tail2 := tail2 + 1;
                                head := head + 3;
                            else 
                                buffer2(tail2) := buffer1(head);
                                tail2 := tail2 + 1;
                                head := head + 1;
                                buffer2(tail2) := buffer1(head);
                                head := head + 1;
                                tail2 := tail2 + 1;
                                buffer2(tail2) := buffer1(head);
                                head := head + 1;
                                tail2 := tail2 + 1;
                            end if;
                                
                      
                        elsif ((keyValue(buffer1(head + 1))- keyValue(buffer1(head))) mod 12) = 5 then
                            if ((keyValue(buffer1(head + 2))- keyValue(buffer1(head + 1))) mod 12) = 2 then
                                buffer2(tail2) := buffer1(head);
                                tail2 := tail2 + 1;
                                buffer2(tail2) := "01110011";
                                tail2 := tail2 + 1;
                                head := head + 3;
                            else
                                buffer2(tail2) := buffer1(head);
                                tail2 := tail2 + 1;
                                head := head + 1;
                                buffer2(tail2) := buffer1(head);
                                head := head + 1;
                                tail2 := tail2 + 1;
                                buffer2(tail2) := buffer1(head);
                                head := head + 1;
                                tail2 := tail2 + 1;
                            end if;
                        
                        else
                            buffer2(tail2) := buffer1(head);
                            tail2 := tail2 + 1;
                            head := head + 1;
                            buffer2(tail2) := buffer1(head);
                            head := head + 1;
                            tail2 := tail2 + 1;
                            buffer2(tail2) := buffer1(head);
                            head := head + 1;
                            tail2 := tail2 + 1;
                               
                                
                        end if;
                    
                    elsif tail = head + 4 then
                        if ((keyValue(buffer1(head + 1))- keyValue(buffer1(head))) mod 12) = 4 and ((keyValue(buffer1(head + 2))- keyValue(buffer1(head + 1))) mod 12) = 3  then
                            if ((keyValue(buffer1(head + 3))- keyValue(buffer1(head + 2))) mod 12) = 3 then
                                buffer2(tail2) := buffer1(head);
                                tail2 := tail2 + 1;
                                buffer2(tail2) := "00110111";
                                tail2 := tail2 + 1;
                                head := head + 4;
                            else
                                buffer2(tail2) := buffer1(head);
                                tail2 := tail2 + 1;
                                buffer2(tail2) := "01001101";
                                tail2 := tail2 + 1;
                                head := head + 3;
                                buffer2(tail2) := buffer1(head);
                                tail2 := tail2 + 1;
                                head := head + 1;
                            end if;
                        
                        elsif ((keyValue(buffer1(head + 1))- keyValue(buffer1(head))) mod 12) = 3 and ((keyValue(buffer1(head + 2))- keyValue(buffer1(head + 1))) mod 12) = 4 then
                                buffer2(tail2) := buffer1(head);
                                tail2 := tail2 + 1;
                                buffer2(tail2) := "01101101";
                                tail2 := tail2 + 1;
                                head := head + 3;
                                buffer2(tail2) := buffer1(head);
                                tail2 := tail2 + 1;
                                head := head + 1;
                                    
                          
                        elsif ((keyValue(buffer1(head + 1))- keyValue(buffer1(head))) mod 12) = 5 and ((keyValue(buffer1(head + 2))- keyValue(buffer1(head + 1))) mod 12) = 2 then
                                buffer2(tail2) := buffer1(head);
                                tail2 := tail2 + 1;
                                buffer2(tail2) := "01110011";
                                tail2 := tail2 + 1;
                                head := head + 3;
                                buffer2(tail2) := buffer1(head);
                                tail2 := tail2 + 1;
                                head := head + 1;

                        else 
                            buffer2(tail2) := buffer1(head);
                            tail2 := tail2 + 1;
                            head := head + 1;
                            buffer2(tail2) := buffer1(head);
                            head := head + 1;
                            tail2 := tail2 + 1;
                            buffer2(tail2) := buffer1(head);
                            head := head + 1;
                            tail2 := tail2 + 1;
                            buffer2(tail2) := buffer1(head);
                            head := head + 1;
                            tail2 := tail2 + 1;
                            
                        end if;
                    
                    elsif tail = head + 5 then
                        
                        if ((keyValue(buffer1(head + 3))- keyValue(buffer1(head + 2))) mod 12) = 3 then
                            buffer2(tail2) := buffer1(head);
                            tail2 := tail2 + 1;
                            buffer2(tail2) := "00110111";
                            tail2 := tail2 + 1;
                            head := head + 4;
                            buffer2(tail2) := buffer1(head);
                            tail2 := tail2 + 1;
                            head := head + 1;
                        
                        else 
                            buffer2(tail2) := buffer1(head);
                            tail2 := tail2 + 1;
                            buffer2(tail2) := "01001101";
                            tail2 := tail2 + 1;
                            head := head + 3;
                            buffer2(tail2) := buffer1(head);
                            tail2 := tail2 + 1;
                            head := head + 1;
                            buffer2(tail2) := buffer1(head);
                            tail2 := tail2 + 1;
                            head := head + 1;

                        
                        end if;
                        
            


                    end if;



                else
                    
                    if tail = head + 3 then
                        
                        if ((keyValue(buffer1(head + 1))- keyValue(buffer1(head))) mod 12) /= 3 and ((keyValue(buffer1(head + 1))- keyValue(buffer1(head))) mod 12) /= 4 and ((keyValue(buffer1(head + 1))- keyValue(buffer1(head))) mod 12) /= 5 then
                            buffer2(tail2) := buffer1(head);
                            head := head + 1;
                            tail2 := tail2 + 1;
                        
                        end if;
                    elsif tail = head + 4 then
                        
                        if ((keyValue(buffer1(head + 1))- keyValue(buffer1(head))) mod 12) = 4 and ((keyValue(buffer1(head + 2))- keyValue(buffer1(head+1))) mod 12) /= 3 then
                            buffer2(tail2) := buffer1(head);
                            head := head + 1;
                            tail2 := tail2 + 1;
                            if ((keyValue(buffer1(head + 1))- keyValue(buffer1(head))) mod 12) /= 3 and ((keyValue(buffer1(head + 1))- keyValue(buffer1(head))) mod 12) /= 4 and ((keyValue(buffer1(head + 1))- keyValue(buffer1(head))) mod 12) /= 5 then
                                buffer2(tail2) := buffer1(head);
                                head := head + 1;
                                tail2 := tail2 + 1;
                            
                            end if;
                        end if;

                        if ((keyValue(buffer1(head + 1))- keyValue(buffer1(head))) mod 12) = 3 then
                            
                            if ((keyValue(buffer1(head + 2))- keyValue(buffer1(head + 1))) mod 12) = 4 then
                                buffer2(tail2) := buffer1(head);
                                tail2 := tail2 + 1;
                                buffer2(tail2) := "01101101";
                                tail2 := tail2 + 1;
                                head := head + 3;
                              
                            
                            else 
                               buffer2(tail2) := buffer1(head);
                               head := head + 1;
                               tail2 := tail2 + 1;
                               if ((keyValue(buffer1(head + 1))- keyValue(buffer1(head))) mod 12) /= 3 and ((keyValue(buffer1(head + 1))- keyValue(buffer1(head))) mod 12) /= 4 and ((keyValue(buffer1(head + 1))- keyValue(buffer1(head))) mod 12) /= 5 then
                                   buffer2(tail2) := buffer1(head);
                                   head := head + 1;
                                   tail2 := tail2 + 1;
                               
                               end if;
                            
                            end if;
                        end if;
                      
                        if ((keyValue(buffer1(head + 1))- keyValue(buffer1(head))) mod 12) = 5 then
                            if ((keyValue(buffer1(head + 2))- keyValue(buffer1(head + 1))) mod 12) = 2 then
                                buffer2(tail2) := buffer1(head);
                                tail2 := tail2 + 1;
                                buffer2(tail2) := "01110011";
                                tail2 := tail2 + 1;
                                head := head + 3;
                                
                            
                            else 
                                buffer2(tail2) := buffer1(head);
                                head := head + 1;
                                tail2 := tail2 + 1;
                                if ((keyValue(buffer1(head + 1))- keyValue(buffer1(head))) mod 12) /= 3 and ((keyValue(buffer1(head + 1))- keyValue(buffer1(head))) mod 12) /= 4 and ((keyValue(buffer1(head + 1))- keyValue(buffer1(head))) mod 12) /= 5 then
                                    buffer2(tail2) := buffer1(head);
                                    head := head + 1;
                                    tail2 := tail2 + 1;
                            
                                end if;
                            
                            end if;
                            

                        
                        end if;


                    elsif tail = head + 5 then

                        if ((keyValue(buffer1(head + 1))- keyValue(buffer1(head))) mod 12) = 4 and ((keyValue(buffer1(head + 2))- keyValue(buffer1(head + 1))) mod 12) = 3 then
                            
                            if ((keyValue(buffer1(head + 3))- keyValue(buffer1(head + 2))) mod 12) = 3 then
                                buffer2(tail2) := buffer1(head);
                                tail2 := tail2 + 1;
                                buffer2(tail2) := "00110111";
                                tail2 := tail2 + 1;
                                head := head + 4;
                            
                            else 
                                buffer2(tail2) := buffer1(head);
                                tail2 := tail2 + 1;
                                buffer2(tail2) := "01001101";
                                tail2 := tail2 + 1;
                                head := head + 3;
                            
                            end if;
                        end if;
                    
                    end if;
                    
                    buffer1(tail) := a;
                    tail := tail + 1;
                
                end if;
                
                if head2 < tail2 then
                    data_valid <= '1';
                    z <= std_logic_vector(buffer2(head2));
                    head2 := head2 + 1;
                
                else
                    data_valid <= '0';
                    z <= "00000000";
                
                end if;
            
            end if;

    end process;

end behavior;