int test() {
    char a = 5;
    a = a + 3;
    return a;
}

char a = 5;         lda     #$05
                    jsr     pusha

            
a = a + 3;          ldy     #$00
                    lda     (c_sp),y
                    clc
                    adc     #$03
                    sta     (c_sp),y

return a;           ldx     #$00
                    lda     (c_sp),y

}                   jmp     incsp1

