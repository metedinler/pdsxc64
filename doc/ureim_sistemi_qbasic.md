### **2. QBasic Language Features Analysis**

#### **A) Variable Types and Declarations**
```qbasic
' QBasic strong typing system
DIM playerName$ AS STRING * 20    ' Fixed-length string
DIM score& AS LONG               ' Long integer
DIM health% AS INTEGER           ' Integer
DIM accuracy! AS SINGLE          ' Single-precision float
DIM precision# AS DOUBLE         ' Double-precision float

' Dynamic arrays
DIM gameBoard%(1 TO 10, 1 TO 10)
DIM playerNames$(1 TO 100)
```

**Assembly Variable Mapping:**
```assembly
; C64 Assembly variable storage
player_name:     .fill 20, 0    ; String storage
score_value:     .fill 4, 0     ; Long integer (4 bytes)
health_value:    .word 0        ; Integer (2 bytes)
accuracy_value:  .fill 4, 0     ; Single float (4 bytes)
precision_value: .fill 8, 0     ; Double float (8 bytes)

; Array storage
game_board:      .fill 200, 0   ; 10x10 integer array
player_names:    .fill 2000, 0  ; 100 strings * 20 chars
```

#### **B) QBasic Control Structures**

**Modern Loop Constructs:**
```qbasic
' DO-LOOP structures
DO WHILE condition%
    ' Loop body
LOOP

DO UNTIL condition%
    ' Loop body
LOOP

DO
    ' Loop body
LOOP WHILE condition%

DO
    ' Loop body
LOOP UNTIL condition%

' Enhanced FOR loops
FOR i% = 1 TO 100 STEP 2
    ' Loop body
NEXT i%

' SELECT CASE (modern switch)
SELECT CASE choice%
    CASE 1
        PRINT "Option One"
    CASE 2 TO 5
        PRINT "Options Two through Five"
    CASE IS > 10
        PRINT "Greater than Ten"
    CASE ELSE
        PRINT "Default case"
END SELECT
```

**Assembly Loop Pattern Recognition:**
```assembly
; DO WHILE pattern
do_while_loop:
    ; Test condition first
    LDA condition_var
    CMP #0
    BEQ end_do_while
    
    ; Loop body
    ; ... loop body code ...
    
    JMP do_while_loop
end_do_while:

; DO UNTIL pattern  
do_until_loop:
    ; Test condition first
    LDA condition_var
    CMP #0
    BNE end_do_until
    
    ; Loop body
    ; ... loop body code ...
    
    JMP do_until_loop
end_do_until:

; SELECT CASE pattern
select_case:
    LDA choice_var
    
    CMP #1
    BEQ case_1
    CMP #2
    BCC case_else      ; < 2
    CMP #6
    BCS check_greater  ; >= 6
    JMP case_2_to_5
    
check_greater:
    CMP #11
    BCS case_greater_10
    JMP case_else
    
case_1:
    ; Option One code
    JMP case_end
    
case_2_to_5:
    ; Options Two through Five code
    JMP case_end
    
case_greater_10:
    ; Greater than Ten code
    JMP case_end
    
case_else:
    ; Default case code
    
case_end:
```

#### **C) QBasic Procedures and Functions**

**Advanced Procedure System:**
```qbasic
' Procedure with parameters
SUB DrawSprite (x%, y%, color%, spriteData%())
    FOR row% = 0 TO 7
        FOR col% = 0 TO 7
            IF spriteData%(row%, col%) <> 0 THEN
                PSET (x% + col%, y% + row%), color%
            END IF
        NEXT col%
    NEXT row%
END SUB

' Function with local variables
FUNCTION CalculateDistance! (x1%, y1%, x2%, y2%)
    DIM deltaX%, deltaY%
    DIM distanceSquared&
    
    deltaX% = x2% - x1%
    deltaY% = y2% - y1%
    distanceSquared& = CLng(deltaX%) * deltaX% + CLng(deltaY%) * deltaY%
    
    CalculateDistance! = SQR(distanceSquared&)
END FUNCTION

' Shared variables
DIM SHARED globalScore&, globalLevel%

SUB UpdateScore (points%)
    globalScore& = globalScore& + points%
    IF globalScore& > 10000 THEN globalLevel% = globalLevel% + 1
END SUB
```

**Assembly Procedure Implementation:**
```assembly
; QBasic SUB DrawSprite implementation
DrawSprite:
    ; Parameter stack: x%, y%, color%, spriteData%() pointer
    ; Save registers
    PHA
    TXA
    PHA
    TYA
    PHA
    
    ; Load parameters from stack/memory
    LDA param_x
    STA local_x
    LDA param_y
    STA local_y
    LDA param_color
    STA local_color
    
    ; Nested loop implementation
    LDA #0              ; row% = 0
    STA loop_row
    
outer_loop:
    LDA #0              ; col% = 0
    STA loop_col
    
inner_loop:
    ; Calculate array index: row% * 8 + col%
    LDA loop_row
    ASL A               ; * 2
    ASL A               ; * 4  
    ASL A               ; * 8
    CLC
    ADC loop_col
    TAY
    
    ; Load spriteData%(row%, col%)
    LDA (sprite_data_ptr),Y
    CMP #0
    BEQ skip_pixel
    
    ; PSET (x% + col%, y% + row%), color%
    LDA local_x
    CLC
    ADC loop_col
    STA pixel_x
    
    LDA local_y
    CLC
    ADC loop_row
    STA pixel_y
    
    LDA local_color
    JSR plot_pixel      ; Call graphics routine
    
skip_pixel:
    ; Next col%
    INC loop_col
    LDA loop_col
    CMP #8
    BCC inner_loop
    
    ; Next row%
    INC loop_row
    LDA loop_row
    CMP #8
    BCC outer_loop
    
    ; Restore registers and return
    PLA
    TAY
    PLA
    TAX
    PLA
    RTS

; Local variables storage
local_x:        .byte 0
local_y:        .byte 0
local_color:    .byte 0
loop_row:       .byte 0
loop_col:       .byte 0
pixel_x:        .byte 0
pixel_y:        .byte 0
