.model small
.stack 100h

.data
    str_1  DB '', 0Dh, 0Ah, '$'
    str_0  DB '===== EJEMPLO DE DICCIONARIOS =====', 0Dh, 0Ah, '$'
    str_12 DB '===== FIN =====', 0Dh, 0Ah, '$'
    str_9  DB 'Actualizando stock del producto 1...', 0Dh, 0Ah, '$'
    str_5  DB 'Calculando valor del producto 1...', 0Dh, 0Ah, '$'
    str_2  DB 'Creando producto con diccionario...', 0Dh, 0Ah, '$'
    str_3  DB 'Producto creado:', 0Dh, 0Ah, '$'
    str_4  DB 'Segundo producto:', 0Dh, 0Ah, '$'
    str_10 DB 'Stock anterior:', 0Dh, 0Ah, '$'
    str_11 DB 'Stock nuevo:', 0Dh, 0Ah, '$'
    str_8  DB 'Valor total de inventario:', 0Dh, 0Ah, '$'
    str_6  DB 'Valor total del Producto 1:', 0Dh, 0Ah, '$'
    str_7  DB 'Valor total del Producto 2:', 0Dh, 0Ah, '$'

    newline DB 0Dh,0Ah,'$'

    input_buffer DB 6, ?, 6 DUP(?)

    LaptopStr DB "Laptop",0
    MouseStr  DB "Mouse",0

    dict_open         DB "{'desc': '",0
    dict_comma_precio DB "', 'precio': ",0
    dict_comma_stock  DB ", 'stock': ",0
    dict_close        DB "}",0

    t0_desc   DW 0
    t0_precio DW 0
    t0_stock  DW 0

    t1_desc   DW 0
    t1_precio DW 0
    t1_stock  DW 0

    producto1        DW 0
    producto1_precio DW 0
    producto1_stock  DW 0

    producto2        DW 0
    producto2_precio DW 0
    producto2_stock  DW 0

    t0   DW 0
    t1   DW 0
    t2   DW 0
    t3   DW 0
    t4   DW 0
    t5   DW 0
    t6   DW 0
    t7   DW 0
    t8   DW 0
    t9   DW 0
    t10  DW 0
    t11  DW 0
    t12  DW 0
    total  DW 0
    valor1 DW 0
    valor2 DW 0

.code

main PROC
    MOV AX, @data
    MOV DS, AX

    MOV DX, OFFSET str_0
    MOV AH, 09h
    INT 21h
    MOV DX, OFFSET str_1
    MOV AH, 09h
    INT 21h
    MOV DX, OFFSET str_2
    MOV AH, 09h
    INT 21h

    ; t0 = {}
    MOV AX, OFFSET t0
    MOV t0, AX

    ; t0["desc"] = "Laptop"
    MOV BX, OFFSET LaptopStr
    MOV t0_desc, BX

    ; t0["precio"] = 1200
    MOV CX, 1200
    MOV t0_precio, CX

    ; t0["stock"] = 5
    MOV DX, 5
    MOV t0_stock, DX

    ; producto1 = t0
    MOV SI, t0
    MOV producto1, SI

    ; copiar a producto1_*
    MOV AX, t0_precio
    MOV producto1_precio, AX
    MOV BX, t0_stock
    MOV producto1_stock, BX

    MOV DX, OFFSET str_3
    MOV AH, 09h
    INT 21h

    ; print(producto1)
    MOV BX, t0_desc
    MOV CX, producto1_precio
    MOV DX, producto1_stock
    CALL print_dict
    MOV DX, OFFSET str_1
    MOV AH, 09h
    INT 21h

    ; t1 = {}
    MOV AX, OFFSET t1
    MOV t1, AX

    ; t1["desc"] = "Mouse"
    MOV BX, OFFSET MouseStr
    MOV t1_desc, BX

    ; t1["precio"] = 25
    MOV CX, 25
    MOV t1_precio, CX

    ; t1["stock"] = 20
    MOV DX, 20
    MOV t1_stock, DX

    ; producto2 = t1
    MOV SI, t1
    MOV producto2, SI

    ; copiar a producto2_*
    MOV AX, t1_precio
    MOV producto2_precio, AX
    MOV BX, t1_stock
    MOV producto2_stock, BX

    MOV DX, OFFSET str_4
    MOV AH, 09h
    INT 21h

    ; print(producto2)
    MOV BX, t1_desc
    MOV CX, producto2_precio
    MOV DX, producto2_stock
    CALL print_dict
    MOV DX, OFFSET str_1
    MOV AH, 09h
    INT 21h

    MOV DX, OFFSET str_5
    MOV AH, 09h
    INT 21h

    ; t2 = producto1["precio"]
    MOV AX, producto1_precio
    MOV t2, AX

    ; t3 = producto1["stock"]
    MOV BX, producto1_stock
    MOV t3, BX

    ; t4 = t2 * t3
    MOV CX, t2
    MOV DX, t3
    MOV AX, CX
    MUL DX
    MOV t4, AX

    ; valor1 = t4
    MOV AX, t4
    MOV valor1, AX

    MOV DX, OFFSET str_6
    MOV AH, 09h
    INT 21h
    MOV AX, valor1
    CALL print_number_inline
    MOV DX, OFFSET str_1
    MOV AH, 09h
    INT 21h

    ; t5 = producto2["precio"]
    MOV AX, producto2_precio
    MOV t5, AX

    ; t6 = producto2["stock"]
    MOV AX, producto2_stock
    MOV t6, AX

    ; t7 = t5 * t6
    MOV BX, t5
    MOV CX, t6
    MOV AX, BX
    MUL CX
    MOV t7, AX

    ; valor2 = t7
    MOV AX, t7
    MOV valor2, AX

    MOV DX, OFFSET str_7
    MOV AH, 09h
    INT 21h
    MOV AX, valor2
    CALL print_number_inline
    MOV DX, OFFSET str_1
    MOV AH, 09h
    INT 21h

    ; t8 = valor1 + valor2
    MOV AX, valor1
    MOV BX, valor2
    ADD AX, BX
    MOV t8, AX

    ; total = t8
    MOV total, AX

    MOV DX, OFFSET str_8
    MOV AH, 09h
    INT 21h
    MOV AX, total
    CALL print_number_inline
    MOV DX, OFFSET str_1
    MOV AH, 09h
    INT 21h

    MOV DX, OFFSET str_9
    MOV AH, 09h
    INT 21h
    MOV DX, OFFSET str_10
    MOV AH, 09h
    INT 21h

    ; t9 = producto1["stock"]
    MOV AX, producto1_stock
    MOV t9, AX
    MOV AX, t9
    CALL print_number_inline

    ; t10 = producto1["stock"]
    MOV AX, producto1_stock
    MOV t10, AX

    ; t11 = t10 + 3
    MOV AX, t10
    ADD AX, 3
    MOV t11, AX

    ; producto1["stock"] = t11
    MOV AX, t11
    MOV producto1_stock, AX

    MOV DX, OFFSET str_11
    MOV AH, 09h
    INT 21h

    ; t12 = producto1["stock"]
    MOV AX, producto1_stock
    MOV t12, AX
    MOV AX, t12
    CALL print_number_inline

    MOV DX, OFFSET str_1
    MOV AH, 09h
    INT 21h
    MOV DX, OFFSET str_12
    MOV AH, 09h
    INT 21h

    MOV AH, 4Ch
    INT 21h
main ENDP

;-------------------------------------------------------
; Imprime cadena C-terminada (0)
; Entrada: DS:SI -> cadena terminada en 0
;   *Ahora preserva DX para no romper valores numéricos*
;-------------------------------------------------------
print_cstring PROC
    PUSH AX
    PUSH DX
pc_loop:
    MOV AL, [SI]
    CMP AL, 0
    JE pc_done
    MOV DL, AL
    MOV AH, 02h
    INT 21h
    INC SI
    JMP pc_loop
pc_done:
    POP DX
    POP AX
    RET
print_cstring ENDP

;-------------------------------------------------------
; Imprime "diccionario" con formato:
; {'desc': <BX-string>, 'precio': <CX>, 'stock': <DX>}
;-------------------------------------------------------
print_dict PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    PUSH SI

    ; "{'desc': '"
    MOV SI, OFFSET dict_open
    CALL print_cstring

    ; desc
    MOV SI, BX
    CALL print_cstring

    ; "', 'precio': "
    MOV SI, OFFSET dict_comma_precio
    CALL print_cstring

    ; precio (CX)
    MOV AX, CX
    CALL print_number_inline

    ; ", 'stock': "
    MOV SI, OFFSET dict_comma_stock
    CALL print_cstring

    ; stock (DX)  -> DX sigue intacto gracias a print_cstring
    MOV AX, DX
    CALL print_number_inline

    ; "}"
    MOV SI, OFFSET dict_close
    CALL print_cstring

    POP SI
    POP DX
    POP CX
    POP BX
    POP AX
    RET
print_dict ENDP

;-------------------------------------------------------
; Convierte cadena en SI -> AX (entero) [no usado aquí]
;-------------------------------------------------------
string_to_int PROC
    PUSH BX
    PUSH CX
    PUSH DX
    XOR AX, AX
    MOV CX, 10
s2i_loop:
    MOV BL, [SI]
    CMP BL, 0
    JE s2i_done
    CMP BL, '0'
    JL s2i_done
    CMP BL, '9'
    JG s2i_done
    SUB BL, '0'
    MOV BH, 0
    MUL CX
    ADD AX, BX
    INC SI
    JMP s2i_loop
s2i_done:
    POP DX
    POP CX
    POP BX
    RET
string_to_int ENDP

;-------------------------------------------------------
; Imprime número en AX (base 10)
;-------------------------------------------------------
print_number_inline PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    PUSH SI

    MOV CX, 0
    MOV BX, 10
    CMP AX, 0
    JGE pn_loop
    NEG AX
    PUSH AX
    MOV DL, '-'
    MOV AH, 02h
    INT 21h
    POP AX
pn_loop:
    XOR DX, DX
    DIV BX
    PUSH DX
    INC CX
    CMP AX, 0
    JNE pn_loop
pn_digits:
    POP DX
    ADD DL, '0'
    MOV AH, 02h
    INT 21h
    LOOP pn_digits

    POP SI
    POP DX
    POP CX
    POP BX
    POP AX
    RET
print_number_inline ENDP

END main
