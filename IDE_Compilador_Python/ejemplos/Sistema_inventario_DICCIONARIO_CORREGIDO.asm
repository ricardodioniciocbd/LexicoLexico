.model small
.stack 100h

.data
    ; ===== Cadenas de texto =====
    str_1 DB '', 0Dh, 0Ah, '$'
    str_0 DB '===== EJEMPLO DE DICCIONARIOS =====', 0Dh, 0Ah, '$'
    str_12 DB '===== FIN =====', 0Dh, 0Ah, '$'
    str_9 DB 'Actualizando stock del producto 1...', 0Dh, 0Ah, '$'
    str_5 DB 'Calculando valor del producto 1...', 0Dh, 0Ah, '$'
    str_2 DB 'Creando producto con diccionario...', 0Dh, 0Ah, '$'
    str_3 DB 'Producto creado:', 0Dh, 0Ah, '$'
    str_4 DB 'Segundo producto:', 0Dh, 0Ah, '$'
    str_10 DB 'Stock anterior:', 0Dh, 0Ah, '$'
    str_11 DB 'Stock nuevo:', 0Dh, 0Ah, '$'
    str_8 DB 'Valor total de inventario:', 0Dh, 0Ah, '$'
    str_6 DB 'Valor total del Producto 1:', 0Dh, 0Ah, '$'
    str_7 DB 'Valor total del Producto 2:', 0Dh, 0Ah, '$'

    newline DB 0Dh,0Ah,'$'

    ; ===== Etiquetas para strings de datos =====
    LaptopStr DB "Laptop",0
    MouseStr DB "Mouse",0

    ; ===== Variables del programa =====
    t4_buffer DB 6, ?, 6 DUP(?)   ; buffer de entrada
    
    ; Variables base de diccionarios
    producto1 DW 0
    producto2 DW 0
    t0 DW 0
    t1 DW 0
    
    ; Campos del diccionario t0
    t0_desc DW 0
    t0_precio DW 0
    t0_stock DW 0
    
    ; Campos del diccionario t1
    t1_desc DW 0
    t1_precio DW 0
    t1_stock DW 0
    
    ; Campos del diccionario producto1
    producto1_desc DW 0
    producto1_precio DW 0
    producto1_stock DW 0
    
    ; Campos del diccionario producto2
    producto2_desc DW 0
    producto2_precio DW 0
    producto2_stock DW 0
    
    ; Variables temporales
    t2 DW 0
    t3 DW 0
    t5 DW 0
    t6 DW 0
    t7 DW 0
    t8 DW 0
    t9 DW 0
    t10 DW 0
    t11 DW 0
    t12 DW 0
    
    ; Variables finales
    total DW 0
    valor1 DW 0
    valor2 DW 0


.code

main PROC
    MOV AX, @data
    MOV DS, AX

    ; ===== EJEMPLO DE DICCIONARIOS =====
    MOV DX, OFFSET str_0
    MOV AH, 09h
    INT 21h
    
    ; Línea vacía
    MOV DX, OFFSET str_1
    MOV AH, 09h
    INT 21h
    
    ; Creando producto con diccionario...
    MOV DX, OFFSET str_2
    MOV AH, 09h
    INT 21h
    
    ; ===== Crear diccionario t0 =====
    ; t0 = {} (crear diccionario)
    MOV AX, OFFSET t0
    MOV t0, AX
    
    ; t0["desc"] = "Laptop"
    MOV BX, OFFSET LaptopStr    ; Cargar dirección de "Laptop"
    MOV t0_desc, BX             ; Asignar t0_desc
    
    ; t0["precio"] = 1200
    MOV CX, 1200                ; Cargar constante 1200
    MOV t0_precio, CX           ; Asignar t0_precio
    
    ; t0["stock"] = 5
    MOV DX, 5                   ; Cargar constante 5
    MOV t0_stock, DX            ; Asignar t0_stock
    
    ; producto1 = t0 (copiar referencias)
    MOV AX, t0_desc
    MOV producto1_desc, AX
    MOV AX, t0_precio
    MOV producto1_precio, AX
    MOV AX, t0_stock
    MOV producto1_stock, AX
    
    ; Producto creado:
    MOV DX, OFFSET str_3
    MOV AH, 09h
    INT 21h
    
    ; Imprimir producto1 (simplificado: imprimir 0)
    MOV AX, producto1
    CALL print_number_inline
    
    ; Línea vacía
    MOV DX, OFFSET str_1
    MOV AH, 09h
    INT 21h
    
    ; ===== Crear diccionario t1 =====
    ; t1 = {} (crear diccionario)
    MOV SI, OFFSET t1
    MOV t1, SI
    
    ; t1["desc"] = "Mouse"
    MOV DI, OFFSET MouseStr     ; Cargar dirección de "Mouse"
    MOV t1_desc, DI             ; Asignar t1_desc
    
    ; t1["precio"] = 25
    MOV AX, 25                  ; Cargar constante 25
    MOV t1_precio, AX           ; Asignar t1_precio
    
    ; t1["stock"] = 20
    MOV BX, 20                  ; Cargar constante 20
    MOV t1_stock, BX            ; Asignar t1_stock
    
    ; producto2 = t1 (copiar referencias)
    MOV AX, t1_desc
    MOV producto2_desc, AX
    MOV AX, t1_precio
    MOV producto2_precio, AX
    MOV AX, t1_stock
    MOV producto2_stock, AX
    
    ; Segundo producto:
    MOV DX, OFFSET str_4
    MOV AH, 09h
    INT 21h
    
    ; Imprimir producto2 (simplificado: imprimir 0)
    MOV AX, producto2
    CALL print_number_inline
    
    ; Línea vacía
    MOV DX, OFFSET str_1
    MOV AH, 09h
    INT 21h
    
    ; ===== Calcular valor del producto 1 =====
    ; Calculando valor del producto 1...
    MOV DX, OFFSET str_5
    MOV AH, 09h
    INT 21h
    
    ; t2 = producto1["precio"]
    MOV CX, producto1_precio    ; Cargar producto1_precio
    MOV t2, CX                  ; Almacenar en t2
    
    ; t3 = producto1["stock"]
    MOV DX, producto1_stock     ; Cargar producto1_stock
    MOV t3, DX                  ; Almacenar en t3
    
    ; t4 = t2 * t3 (pero t4 es buffer, usar otra variable)
    ; valor1 = t2 * t3
    MOV AX, t2                  ; Cargar t2 en AX
    MOV BX, t3                  ; Cargar t3 en BX
    MUL BX                      ; AX = AX * BX
    MOV valor1, AX              ; Almacenar resultado en valor1
    
    ; Valor total del Producto 1:
    MOV DX, OFFSET str_6
    MOV AH, 09h
    INT 21h
    
    ; Imprimir valor1
    MOV AX, valor1
    CALL print_number_inline
    
    ; Línea vacía
    MOV DX, OFFSET str_1
    MOV AH, 09h
    INT 21h
    
    ; ===== Calcular valor del producto 2 =====
    ; t5 = producto2["precio"]
    MOV BX, producto2_precio    ; Cargar producto2_precio
    MOV t5, BX                  ; Almacenar en t5
    
    ; t6 = producto2["stock"]
    MOV CX, producto2_stock     ; Cargar producto2_stock
    MOV t6, CX                  ; Almacenar en t6
    
    ; t7 = t5 * t6
    MOV AX, t5                  ; Cargar t5 en AX
    MOV BX, t6                  ; Cargar t6 en BX
    MUL BX                      ; AX = AX * BX
    MOV t7, AX                  ; Almacenar en t7
    
    ; valor2 = t7
    MOV AX, t7                  ; Cargar t7
    MOV valor2, AX              ; Almacenar en valor2
    
    ; Valor total del Producto 2:
    MOV DX, OFFSET str_7
    MOV AH, 09h
    INT 21h
    
    ; Imprimir valor2
    MOV AX, valor2
    CALL print_number_inline
    
    ; Línea vacía
    MOV DX, OFFSET str_1
    MOV AH, 09h
    INT 21h
    
    ; ===== Calcular valor total =====
    ; t8 = valor1 + valor2
    MOV AX, valor1              ; Cargar valor1
    MOV BX, valor2              ; Cargar valor2
    ADD AX, BX                  ; AX = AX + BX
    MOV t8, AX                  ; Almacenar en t8
    
    ; total = t8
    MOV AX, t8                  ; Cargar t8
    MOV total, AX               ; Almacenar en total
    
    ; Valor total de inventario:
    MOV DX, OFFSET str_8
    MOV AH, 09h
    INT 21h
    
    ; Imprimir total
    MOV AX, total
    CALL print_number_inline
    
    ; Línea vacía
    MOV DX, OFFSET str_1
    MOV AH, 09h
    INT 21h
    
    ; ===== Actualizar stock =====
    ; Actualizando stock del producto 1...
    MOV DX, OFFSET str_9
    MOV AH, 09h
    INT 21h
    
    ; Stock anterior:
    MOV DX, OFFSET str_10
    MOV AH, 09h
    INT 21h
    
    ; t9 = producto1["stock"]
    MOV BX, producto1_stock     ; Cargar producto1_stock
    MOV t9, BX                  ; Almacenar en t9
    
    ; Imprimir stock anterior (t9)
    MOV AX, t9
    CALL print_number_inline
    
    ; Línea vacía
    MOV DX, OFFSET str_1
    MOV AH, 09h
    INT 21h
    
    ; t10 = producto1["stock"]
    MOV CX, producto1_stock     ; Cargar producto1_stock
    MOV t10, CX                 ; Almacenar en t10
    
    ; t11 = t10 + 3
    MOV AX, t10                 ; Cargar t10
    ADD AX, 3                   ; Sumar 3
    MOV t11, AX                 ; Almacenar en t11
    
    ; producto1["stock"] = t11
    MOV AX, t11                 ; Cargar t11
    MOV producto1_stock, AX     ; Actualizar producto1_stock
    
    ; Stock nuevo:
    MOV DX, OFFSET str_11
    MOV AH, 09h
    INT 21h
    
    ; t12 = producto1["stock"]
    MOV CX, producto1_stock     ; Cargar producto1_stock
    MOV t12, CX                 ; Almacenar en t12
    
    ; Imprimir stock nuevo (t12)
    MOV AX, t12
    CALL print_number_inline
    
    ; Línea vacía
    MOV DX, OFFSET str_1
    MOV AH, 09h
    INT 21h
    
    ; ===== FIN =====
    MOV DX, OFFSET str_12
    MOV AH, 09h
    INT 21h

    ; Terminar programa
    MOV AH, 4Ch
    INT 21h
main ENDP

;-------------------------------------------------------
; Convierte cadena en SI -> AX (entero)
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
; Imprime número (AX)
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

