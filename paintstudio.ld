SECTIONS
{
    __romPos = 0;

    /* 0x00000000 0-40 (len 40) */
    #ifdef SHIFT
    data_0_ROM_START = __romPos;
    #else
    data_0_ROM_START = 0x0;
    #endif
    data_0_VRAM = ADDR(.data_0);
    .data_0 0x0 : AT(data_0_ROM_START) {
        BUILD_DIR/bin/header.o(.data);
    }
    #ifdef SHIFT
    data_0_ROM_END = __romPos + SIZEOF(.data_0);
    __romPos += SIZEOF(.data_0);
    #else
    data_0_ROM_END = 0x40;
    __romPos += 0x40;
    #endif
    
    /* 0x00000000 40-10E8 (len 10A8) */
    #ifdef SHIFT
    data_40_ROM_START = __romPos;
    #else
    data_40_ROM_START = 0x40;
    #endif
    data_40_VRAM = ADDR(.data_40);
    .data_40 0x40 : AT(data_40_ROM_START) {
        BUILD_DIR/bin/boot.o(.data);
    }
    #ifdef SHIFT
    data_40_ROM_END = __romPos + SIZEOF(.data_40);
    __romPos += SIZEOF(.data_40);
    #else
    data_40_ROM_END = 0x10E8;
    __romPos += 0x10A8;
    #endif
    
    /* 0x80000400 10E8-DB27C (len DA194) */
    #ifdef SHIFT
    code_app_ROM_START = __romPos;
    #else
    code_app_ROM_START = 0x10E8;
    #endif
    code_app_VRAM = ADDR(.code_app);
    .code_app 0x80000400 : AT(code_app_ROM_START) {
        BUILD_DIR/asm/app_10E8.o(.text);
        BUILD_DIR/asm/bootproc.o(.text);
        BUILD_DIR/bin/app_129F0.o(.data);
        BUILD_DIR/asm/app_159F8.o(.text);
        BUILD_DIR/bin/app_31148.o(.data);
        BUILD_DIR/asm/app_796B0.o(.text);
    }
    #ifdef SHIFT
    code_app_ROM_END = __romPos + SIZEOF(.code_app);
    __romPos += SIZEOF(.code_app);
    #else
    code_app_ROM_END = 0xDB27C;
    __romPos += 0xDA194;
    #endif
    
}
