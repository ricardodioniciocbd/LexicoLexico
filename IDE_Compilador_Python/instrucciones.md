.model small
.stack 100h

.data
    newline DB 0Dh,0Ah,'$'
    
    ; --- Textos del Menú ---
    str_0 DB 0Dh, 0Ah, '===== PROCESAMIENTO DE CADENAS =====', 0Dh, 0Ah, '$'
    str_1 DB '1. Contar vocales', 0Dh, 0Ah, '$'
    str_2 DB '2. Invertir cadena', 0Dh, 0Ah, '$'
    str_3 DB '3. Verificar palindromo', 0Dh, 0Ah, '$'
    str_4 DB '4. Contar un caracter especifico', 0Dh, 0Ah, '$'
    str_5 DB '5. Convertir a mayusculas', 0Dh, 0Ah, '$'
    str_6 DB '6. Salir', 0Dh, 0Ah, '$'
    
    str_7 DB 0Dh, 0Ah, 'Seleccione una opcion: $'
    str_8 DB 0Dh, 0Ah, 'Ingrese texto: $'
    str_13 DB 0Dh, 0Ah, 'Ingrese caracter a buscar: $'
    
    str_9 DB 0Dh, 0Ah, 'Cantidad de vocales: $'
    str_10 DB 0Dh, 0Ah, 'Invertida: $'
    str_11 DB ' Es palindromo.', 0Dh, 0Ah, '$'
    str_12 DB ' No es palindromo.', 0Dh, 0Ah, '$'
    str_14 DB 0Dh, 0Ah, 'El caracter aparece $'
    str_15 DB ' veces.', 0Dh, 0Ah, '$'
    str_16 DB 0Dh, 0Ah, 'En mayusculas: $'
    str_17 DB 0Dh, 0Ah, 'Saliendo...', 0Dh, 0Ah, '$'
    str_18 DB 0Dh, 0Ah, 'Opcion invalida.', 0Dh, 0Ah, '$'

    ; --- Variables y Buffers ---
    ; IMPORTANTE: Los buffers de entrada deben tener estructura: max_len, actual_len, bytes...
    buffer_opcion DB 5, ?, 5 DUP(0)
    buffer_texto  DB 50, ?, 50 DUP(0)
    buffer_char   DB 5, ?, 5 DUP(0)
    
    ; Punteros y Variables
    texto DW ?          ; Puntero al inicio del string actual
    texto_len DW ?      ; Longitud del texto actual
    
    char_val DW 0       ; Renombrado de 'ch' a 'char_val'
    caracter DW 0       ; Caracter a buscar (ASCII)
    
    contador DW 0
    i DW 0
    
    invertida_buf DB 50 DUP(0), '$' ; Buffer para string invertido
    
    ; Variables temporales del compilador (reutilizadas)
    t0 DW 0
    t1 DW 0

.code

main PROC
    MOV AX, @data
    MOV DS, AX

    CALL user_main

    MOV AH, 4Ch
    INT 21h
main ENDP

; ---------------------------------------------------------
; Función: contar_vocales
; ---------------------------------------------------------
contar_vocales PROC
    MOV contador, 0
    MOV i, 0

L_cv_loop:
    ; Condición bucle: i < len
    MOV AX, i
    CMP AX, texto_len
    JGE L_cv_fin    ; Si i >= len, salir
    
    ; Leer caracter texto[i]
    MOV BX, texto
    ADD BX, i
    MOV AL, [BX]    ; AL tiene el caracter
    MOV AH, 0
    MOV char_val, AX ; Guardar en variable temporal
    
    ; Comparaciones (A, E, I, O, U y minúsculas)
    CMP AL, 'a'
    JE es_vocal
    CMP AL, 'e'
    JE es_vocal
    CMP AL, 'i'
    JE es_vocal
    CMP AL, 'o'
    JE es_vocal
    CMP AL, 'u'
    JE es_vocal
    CMP AL, 'A'
    JE es_vocal
    CMP AL, 'E'
    JE es_vocal
    CMP AL, 'I'
    JE es_vocal
    CMP AL, 'O'
    JE es_vocal
    CMP AL, 'U'
    JE es_vocal
    JMP sig_char

es_vocal:
    INC contador

sig_char:
    INC i
    JMP L_cv_loop

L_cv_fin:
    MOV AX, contador
    RET
contar_vocales ENDP

; ---------------------------------------------------------
; Función: invertir
; Imprime directamente la cadena invertida para simplificar
; ---------------------------------------------------------
invertir PROC
    ; i = len - 1
    MOV AX, texto_len
    DEC AX
    MOV i, AX

L_inv_loop:
    CMP i, 0
    JL L_inv_fin    ; Si i < 0, terminar
    
    ; Imprimir caracter texto[i]
    MOV BX, texto
    ADD BX, i
    MOV DL, [BX]
    MOV AH, 02h
    INT 21h
    
    DEC i
    JMP L_inv_loop

L_inv_fin:
    RET
invertir ENDP

; ---------------------------------------------------------
; Función: es_palindromo
; Retorna 1 en AX si es palíndromo, 0 si no
; ---------------------------------------------------------
es_palindromo PROC
    MOV SI, 0               ; Índice izquierdo
    MOV DI, texto_len
    DEC DI                  ; Índice derecho (len - 1)

L_pal_loop:
    CMP SI, DI
    JGE es_pal_true         ; Si se cruzan, es palíndromo

    ; Cargar char izquierdo
    MOV BX, texto
    ADD BX, SI
    MOV AL, [BX]

    ; Cargar char derecho
    MOV BX, texto
    ADD BX, DI
    MOV AH, [BX]

    CMP AL, AH
    JNE es_pal_false        ; Si son diferentes, no es palíndromo

    INC SI
    DEC DI
    JMP L_pal_loop

es_pal_true:
    MOV AX, 1
    RET

es_pal_false:
    MOV AX, 0
    RET
es_palindromo ENDP

; ---------------------------------------------------------
; Función: contar_caracter
; ---------------------------------------------------------
contar_caracter PROC
    MOV contador, 0
    MOV i, 0

L_cc_loop:
    MOV AX, i
    CMP AX, texto_len
    JGE L_cc_fin

    MOV BX, texto
    ADD BX, i
    MOV AL, [BX]    ; Caracter actual
    MOV AH, 0
    
    MOV CX, caracter ; Caracter a buscar
    CMP AX, CX
    JNE L_cc_next
    INC contador

L_cc_next:
    INC i
    JMP L_cc_loop

L_cc_fin:
    MOV AX, contador
    RET
contar_caracter ENDP

; ---------------------------------------------------------
; Función: a_mayusculas
; Imprime y convierte al vuelo
; ---------------------------------------------------------
a_mayusculas PROC
    MOV i, 0
L_may_loop:
    MOV AX, i
    CMP AX, texto_len
    JGE L_may_fin

    MOV BX, texto
    ADD BX, i
    MOV DL, [BX]    ; Cargar char
    
    ; Si es 'a'...'z', restar 32
    CMP DL, 'a'
    JB print_char
    CMP DL, 'z'
    JA print_char
    SUB DL, 32      ; Convertir a mayúscula

print_char:
    MOV AH, 02h
    INT 21h

    INC i
    JMP L_may_loop

L_may_fin:
    RET
a_mayusculas ENDP


; ---------------------------------------------------------
; LOGICA DEL MENU
; ---------------------------------------------------------
user_main PROC
menu_loop:
    ; Mostrar opciones
    MOV DX, OFFSET str_0
    MOV AH, 09h
    INT 21h
    MOV DX, OFFSET str_1
    MOV AH, 09h
    INT 21h
    MOV DX, OFFSET str_2
    MOV AH, 09h
    INT 21h
    MOV DX, OFFSET str_3
    MOV AH, 09h
    INT 21h
    MOV DX, OFFSET str_4
    MOV AH, 09h
    INT 21h
    MOV DX, OFFSET str_5
    MOV AH, 09h
    INT 21h
    MOV DX, OFFSET str_6
    MOV AH, 09h
    INT 21h
    MOV DX, OFFSET str_7
    MOV AH, 09h
    INT 21h

    ; Leer opción (buffer)
    MOV DX, OFFSET buffer_opcion
    MOV AH, 0Ah
    INT 21h
    
    ; Analizar opción (el char está en buffer+2)
    MOV SI, OFFSET buffer_opcion + 2
    MOV AL, [SI]
    
    CMP AL, '1'
    JE op_1
    CMP AL, '2'
    JE op_2
    CMP AL, '3'
    JE op_3
    CMP AL, '4'
    JE op_4
    CMP AL, '5'
    JE op_5
    CMP AL, '6'
    JE op_6
    
    JMP op_invalida

; --- OPCION 1: Contar Vocales ---
op_1:
    CALL leer_texto_usuario
    MOV DX, OFFSET str_9
    MOV AH, 09h
    INT 21h
    CALL contar_vocales
    CALL print_number
    JMP menu_loop

; --- OPCION 2: Invertir ---
op_2:
    CALL leer_texto_usuario
    MOV DX, OFFSET str_10
    MOV AH, 09h
    INT 21h
    CALL invertir
    JMP menu_loop

; --- OPCION 3: Palíndromo ---
op_3:
    CALL leer_texto_usuario
    CALL es_palindromo
    CMP AX, 1
    JE es_pal
    MOV DX, OFFSET str_12
    MOV AH, 09h
    INT 21h
    JMP menu_loop
es_pal:
    MOV DX, OFFSET str_11
    MOV AH, 09h
    INT 21h
    JMP menu_loop

; --- OPCION 4: Contar Caracter ---
op_4:
    CALL leer_texto_usuario
    
    MOV DX, OFFSET str_13 ; Pedir char
    MOV AH, 09h
    INT 21h
    
    MOV DX, OFFSET buffer_char
    MOV AH, 0Ah
    INT 21h
    
    ; Obtener char ingresado
    MOV SI, OFFSET buffer_char + 2
    MOV AL, [SI]
    MOV AH, 0
    MOV caracter, AX
    
    MOV DX, OFFSET str_14
    MOV AH, 09h
    INT 21h
    
    CALL contar_caracter
    CALL print_number
    
    MOV DX, OFFSET str_15
    MOV AH, 09h
    INT 21h
    JMP menu_loop

; --- OPCION 5: Mayúsculas ---
op_5:
    CALL leer_texto_usuario
    MOV DX, OFFSET str_16
    MOV AH, 09h
    INT 21h
    CALL a_mayusculas
    JMP menu_loop

; --- OPCION 6: Salir ---
op_6:
    MOV DX, OFFSET str_17
    MOV AH, 09h
    INT 21h
    RET

op_invalida:
    MOV DX, OFFSET str_18
    MOV AH, 09h
    INT 21h
    JMP menu_loop

user_main ENDP

; ---------------------------------------------------------
; Helper: Leer texto del usuario y configurar punteros
; ---------------------------------------------------------
leer_texto_usuario PROC
    MOV DX, OFFSET str_8 ; "Ingrese texto"
    MOV AH, 09h
    INT 21h
    
    MOV DX, OFFSET buffer_texto
    MOV AH, 0Ah
    INT 21h
    
    ; Configurar puntero 'texto' al inicio real de los caracteres
    MOV AX, OFFSET buffer_texto + 2
    MOV texto, AX
    
    ; Configurar 'texto_len' leyendo el segundo byte del buffer (cantidad leída)
    MOV SI, OFFSET buffer_texto + 1
    MOV AL, [SI]
    MOV AH, 0
    MOV texto_len, AX
    
    RET
leer_texto_usuario ENDP

; ---------------------------------------------------------
; Helper: Imprimir número en AX
; ---------------------------------------------------------
print_number PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    
    MOV CX, 0
    MOV BX, 10
    
    CMP AX, 0
    JNE loop_div
    ; Si es 0, imprimir 0
    MOV DL, '0'
    MOV AH, 02h
    INT 21h
    JMP fin_print

loop_div:
    MOV DX, 0
    DIV BX      ; AX / 10, Resto en DX
    PUSH DX     ; Guardar dígito
    INC CX
    CMP AX, 0
    JNE loop_div

print_digits:
    POP DX
    ADD DL, '0' ; Convertir a ASCII
    MOV AH, 02h
    INT 21h
    LOOP print_digits

fin_print:
    POP DX
    POP CX
    POP BX
    POP AX
    RET
print_number ENDP

END main