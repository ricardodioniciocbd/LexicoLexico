CÓDIGO ENSAMBLADOR GENERADO
========================================================================================================================

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
    ; contador = 0
    MOV AX, 0    ; Cargar constante 0
    MOV contador, AX    ; Almacenar en contador
    ; i = 0
    MOV CX, 0    ; Cargar constante 0
    MOV i, CX    ; Almacenar en i
L0:
    ; t0 = len()
    MOV AX, texto_len    ; len(texto)
    MOV t0, AX
    ; t1 = i LT t0
    MOV SI, i    ; Cargar i
    MOV DI, t0    ; Cargar t0
    MOV AX, 0    ; Inicializar resultado
    CMP SI, DI
    JL L0_true
    JMP L0_end
L0_true:
    MOV AX, 1
L0_end:
    MOV t1, AX    ; Almacenar en t1
    CMP t1, 0
    JE L1    ; Saltar si falso
    ; t2 = texto[i]
    MOV BX, texto
    ADD BX, i
    MOV AL, [BX]    ; AL tiene el caracter
    MOV AH, 0
    MOV t2, AX ; Guardar en t2
    ; ch = t2
    MOV BX, t2    ; Cargar t2
    MOV ch, BX    ; Almacenar en ch
    ; t3 = ch EQ "a"
    MOV AX, ch
    ; AL tiene el caracter
    CMP AL, 'a'
    JE cmp_true_1
    MOV t3, 0
    JMP cmp_end_1
cmp_true_1:
    MOV t3, 1
cmp_end_1:
    CMP t3, 0
    JE L2    ; Saltar si falso
    ; t4 = contador + 1
    MOV DX, contador    ; Cargar contador
    MOV SI, 1    ; Cargar constante 1
    MOV DI, DX
    ADD DI, SI
    MOV t4, DI
    JMP L3    ; Salto incondicional
L2:
    ; t5 = ch EQ "e"
    MOV AX, ch
    ; AL tiene el caracter
    CMP AL, 'e'
    JE cmp_true_2
    MOV t5, 0
    JMP cmp_end_2
cmp_true_2:
    MOV t5, 1
cmp_end_2:
    CMP t5, 0
    JE L4    ; Saltar si falso
    ; t6 = contador + 1
    MOV AX, contador    ; Cargar contador
    MOV BX, 1    ; Cargar constante 1
    MOV CX, AX
    ADD CX, BX
    MOV t6, CX
    ; contador = t6
    MOV DX, t6    ; Cargar t6
    MOV contador, DX    ; Almacenar en contador
    JMP L3    ; Salto incondicional
L4:
    ; t7 = ch EQ "i"
    MOV AX, ch
    ; AL tiene el caracter
    CMP AL, 'i'
    JE cmp_true_3
    MOV t7, 0
    JMP cmp_end_3
cmp_true_3:
    MOV t7, 1
cmp_end_3:
    CMP t7, 0
    JE L5    ; Saltar si falso
    ; t8 = contador + 1
    MOV SI, contador    ; Cargar contador
    MOV DI, 1    ; Cargar constante 1
    MOV AX, SI
    ADD AX, DI
    MOV t8, AX
    ; contador = t8
    MOV BX, t8    ; Cargar t8
    MOV contador, BX    ; Almacenar en contador
    JMP L3    ; Salto incondicional
L5:
    ; t9 = ch EQ "o"
    MOV AX, ch
    ; AL tiene el caracter
    CMP AL, 'o'
    JE cmp_true_4
    MOV t9, 0
    JMP cmp_end_4
cmp_true_4:
    MOV t9, 1
cmp_end_4:
    CMP t9, 0
    JE L6    ; Saltar si falso
    ; t10 = contador + 1
    MOV CX, contador    ; Cargar contador
    MOV DX, 1    ; Cargar constante 1
    MOV SI, CX
    ADD SI, DX
    MOV t10, SI
    ; contador = t10
    MOV DI, t10    ; Cargar t10
    MOV contador, DI    ; Almacenar en contador
    JMP L3    ; Salto incondicional
L6:
    ; t11 = ch EQ "u"
    MOV AX, ch
    ; AL tiene el caracter
    CMP AL, 'u'
    JE cmp_true_5
    MOV t11, 0
    JMP cmp_end_5
cmp_true_5:
    MOV t11, 1
cmp_end_5:
    CMP t11, 0
    JE L7    ; Saltar si falso
    ; t12 = contador + 1
    MOV AX, contador    ; Cargar contador
    MOV BX, 1    ; Cargar constante 1
    MOV CX, AX
    ADD CX, BX
    MOV t12, CX
    ; contador = t12
    MOV DX, t12    ; Cargar t12
    MOV contador, DX    ; Almacenar en contador
    JMP L3    ; Salto incondicional
L7:
    ; t13 = ch EQ "A"
    MOV AX, ch
    ; AL tiene el caracter
    CMP AL, 'A'
    JE cmp_true_6
    MOV t13, 0
    JMP cmp_end_6
cmp_true_6:
    MOV t13, 1
cmp_end_6:
    CMP t13, 0
    JE L8    ; Saltar si falso
    ; t14 = contador + 1
    MOV SI, contador    ; Cargar contador
    MOV DI, 1    ; Cargar constante 1
    MOV AX, SI
    ADD AX, DI
    MOV t14, AX
    ; contador = t14
    MOV BX, t14    ; Cargar t14
    MOV contador, BX    ; Almacenar en contador
    JMP L3    ; Salto incondicional
L8:
    ; t15 = ch EQ "E"
    MOV AX, ch
    ; AL tiene el caracter
    CMP AL, 'E'
    JE cmp_true_7
    MOV t15, 0
    JMP cmp_end_7
cmp_true_7:
    MOV t15, 1
cmp_end_7:
    CMP t15, 0
    JE L9    ; Saltar si falso
    ; t16 = contador + 1
    MOV CX, contador    ; Cargar contador
    MOV DX, 1    ; Cargar constante 1
    MOV SI, CX
    ADD SI, DX
    MOV t16, SI
    ; contador = t16
    MOV DI, t16    ; Cargar t16
    MOV contador, DI    ; Almacenar en contador
    JMP L3    ; Salto incondicional
L9:
    ; t17 = ch EQ "I"
    MOV AX, ch
    ; AL tiene el caracter
    CMP AL, 'I'
    JE cmp_true_8
    MOV t17, 0
    JMP cmp_end_8
cmp_true_8:
    MOV t17, 1
cmp_end_8:
    CMP t17, 0
    JE L10    ; Saltar si falso
    ; t18 = contador + 1
    MOV AX, contador    ; Cargar contador
    MOV BX, 1    ; Cargar constante 1
    MOV CX, AX
    ADD CX, BX
    MOV t18, CX
    ; contador = t18
    MOV DX, t18    ; Cargar t18
    MOV contador, DX    ; Almacenar en contador
    JMP L3    ; Salto incondicional
L10:
    ; t19 = ch EQ "O"
    MOV AX, ch
    ; AL tiene el caracter
    CMP AL, 'O'
    JE cmp_true_9
    MOV t19, 0
    JMP cmp_end_9
cmp_true_9:
    MOV t19, 1
cmp_end_9:
    CMP t19, 0
    JE L11    ; Saltar si falso
    ; t20 = contador + 1
    MOV SI, contador    ; Cargar contador
    MOV DI, 1    ; Cargar constante 1
    MOV AX, SI
    ADD AX, DI
    MOV t20, AX
    ; contador = t20
    MOV BX, t20    ; Cargar t20
    MOV contador, BX    ; Almacenar en contador
    JMP L3    ; Salto incondicional
L11:
    ; t21 = ch EQ "U"
    MOV AX, ch
    ; AL tiene el caracter
    CMP AL, 'U'
    JE cmp_true_10
    MOV t21, 0
    JMP cmp_end_10
cmp_true_10:
    MOV t21, 1
cmp_end_10:
    CMP t21, 0
    JE L12    ; Saltar si falso
    ; t22 = contador + 1
    MOV CX, contador    ; Cargar contador
    MOV DX, 1    ; Cargar constante 1
    MOV SI, CX
    ADD SI, DX
    MOV t22, SI
    ; contador = t22
    MOV DI, t22    ; Cargar t22
    MOV contador, DI    ; Almacenar en contador
    JMP L3    ; Salto incondicional
L12:
L3:
    ; t23 = i + 1
    MOV AX, i    ; Cargar i
    MOV BX, 1    ; Cargar constante 1
    MOV CX, AX
    ADD CX, BX
    MOV t23, CX
    ; i = t23
    MOV DX, t23    ; Cargar t23
    MOV i, DX    ; Almacenar en i
    JMP L0    ; Salto incondicional
L1:
    MOV SI, contador    ; Cargar contador
    ; return contador
    MOV AX, SI
    RET
contar_vocales ENDP

; ---------------------------------------------------------
; Función: invertir
; ---------------------------------------------------------
invertir PROC
    ; invertida = ""
    ; t24 = len()
    MOV AX, texto_len    ; len(texto)
    MOV t24, AX
    ; t25 = t24 - 1
    MOV DI, t24    ; Cargar t24
    MOV AX, 1    ; Cargar constante 1
    MOV BX, DI
    SUB BX, AX
    MOV t25, BX    ; Almacenar en t25
    ; i = t25
    MOV CX, t25    ; Cargar t25
    MOV i, CX    ; Almacenar en i
L13:
    ; t26 = i GTE 0
    MOV DX, i    ; Cargar i
    MOV SI, 0    ; Cargar constante 0
    MOV DI, 0    ; Inicializar resultado
    CMP DX, SI
    JGE L11_true
    JMP L11_end
L11_true:
    MOV DI, 1
L11_end:
    MOV t26, DI    ; Almacenar en t26
    CMP t26, 0
    JE L14    ; Saltar si falso
    ; t27 = texto[i]
    MOV BX, texto
    ADD BX, i
    MOV AL, [BX]    ; AL tiene el caracter
    MOV AH, 0
    MOV t27, AX ; Guardar en t27
    ; t28 = invertida + t27
    MOV AX, invertida    ; Cargar invertida
    MOV BX, t27    ; Cargar t27
    MOV CX, AX
    ADD CX, BX
    MOV t28, CX
    ; invertida = t28
    MOV DX, t28    ; Cargar t28
    MOV invertida, DX    ; Almacenar en invertida
    ; t29 = i - 1
    MOV DI, i    ; Cargar i
    MOV AX, 1    ; Cargar constante 1
    MOV BX, DI
    SUB BX, AX
    MOV t29, BX    ; Almacenar en t29
    ; i = t29
    MOV CX, t29    ; Cargar t29
    MOV i, CX    ; Almacenar en i
    JMP L13    ; Salto incondicional
L14:
    MOV DX, invertida    ; Cargar invertida
    ; return invertida
    MOV AX, DX
    RET
invertir ENDP

; ---------------------------------------------------------
; Función: es_palindromo
; ---------------------------------------------------------
es_palindromo PROC
    ; t30 = invertir()
    ; Guardar registros antes de llamar función
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    MOV SI, texto    ; Cargar texto
    MOV texto, SI
    CALL invertir
    POP DX
    POP CX
    POP BX
    POP AX
    MOV DI, AX
    MOV t30, DI    ; Almacenar en t30
    ; texto_invertido = t30
    MOV AX, t30    ; Cargar t30
    MOV texto_invertido, AX    ; Almacenar en texto_invertido
    ; t31 = texto_invertido EQ texto
    MOV CX, texto_invertido    ; Cargar texto_invertido
    MOV DX, texto    ; Cargar texto
    MOV SI, 0    ; Inicializar resultado
    CMP CX, DX
    JE L12_true
    JMP L12_end
L12_true:
    MOV SI, 1
L12_end:
    MOV t31, SI    ; Almacenar en t31
    CMP t31, 0
    JE L15    ; Saltar si falso
    MOV DI, 1    ; Cargar constante 1
    ; return 1
    MOV AX, DI
    RET
    JMP L16    ; Salto incondicional
L15:
    MOV AX, 0    ; Cargar constante 0
    ; return 0
    RET
L16:
    ; return None
    MOV AX, 0
    RET
es_palindromo ENDP

; ---------------------------------------------------------
; Función: contar_caracter
; ---------------------------------------------------------
contar_caracter PROC
    ; contador = 0
    MOV BX, 0    ; Cargar constante 0
    MOV contador, BX    ; Almacenar en contador
    ; i = 0
    MOV CX, 0    ; Cargar constante 0
    MOV i, CX    ; Almacenar en i
L17:
    ; t32 = len()
    MOV AX, texto_len    ; len(texto)
    MOV t32, AX
    ; t33 = i LT t32
    MOV DX, i    ; Cargar i
    MOV SI, t32    ; Cargar t32
    MOV DI, 0    ; Inicializar resultado
    CMP DX, SI
    JL L13_true
    JMP L13_end
L13_true:
    MOV DI, 1
L13_end:
    MOV t33, DI    ; Almacenar en t33
    CMP t33, 0
    JE L18    ; Saltar si falso
    ; t34 = texto[i]
    MOV BX, texto
    ADD BX, i
    MOV AL, [BX]    ; AL tiene el caracter
    MOV AH, 0
    MOV t34, AX ; Guardar en t34
    ; t35 = t34 EQ caracter
    MOV AX, t34    ; Cargar t34
    MOV BX, caracter    ; Cargar caracter
    MOV CX, 0    ; Inicializar resultado
    CMP AX, BX
    JE L14_true
    JMP L14_end
L14_true:
    MOV CX, 1
L14_end:
    MOV t35, CX    ; Almacenar en t35
    CMP t35, 0
    JE L19    ; Saltar si falso
    ; t36 = contador + 1
    MOV DX, contador    ; Cargar contador
    MOV SI, 1    ; Cargar constante 1
    MOV DI, DX
    ADD DI, SI
    MOV t36, DI
    ; contador = t36
    MOV AX, t36    ; Cargar t36
    MOV contador, AX    ; Almacenar en contador
    JMP L20    ; Salto incondicional
L19:
L20:
    ; t37 = i + 1
    MOV BX, i    ; Cargar i
    MOV CX, 1    ; Cargar constante 1
    MOV DX, BX
    ADD DX, CX
    MOV t37, DX
    ; i = t37
    MOV SI, t37    ; Cargar t37
    MOV i, SI    ; Almacenar en i
    JMP L17    ; Salto incondicional
L18:
    MOV DI, contador    ; Cargar contador
    ; return contador
    MOV AX, DI
    RET
contar_caracter ENDP

; ---------------------------------------------------------
; Función: convertir_a_mayuscula
; ---------------------------------------------------------
convertir_a_mayuscula PROC
    ; t38 = caracter EQ "a"
    MOV AX, caracter
    ; AL tiene el caracter
    CMP AL, 'a'
    JE cmp_true_15
    MOV t38, 0
    JMP cmp_end_15
cmp_true_15:
    MOV t38, 1
cmp_end_15:
    CMP t38, 0
    JE L21    ; Saltar si falso
    ; return "A"
    MOV AX, 0
    RET
    JMP L22    ; Salto incondicional
L21:
    ; t39 = caracter EQ "b"
    MOV AX, caracter
    ; AL tiene el caracter
    CMP AL, 'b'
    JE cmp_true_16
    MOV t39, 0
    JMP cmp_end_16
cmp_true_16:
    MOV t39, 1
cmp_end_16:
    CMP t39, 0
    JE L23    ; Saltar si falso
    ; return "B"
    MOV AX, 0
    RET
    JMP L22    ; Salto incondicional
L23:
    ; t40 = caracter EQ "c"
    MOV AX, caracter
    ; AL tiene el caracter
    CMP AL, 'c'
    JE cmp_true_17
    MOV t40, 0
    JMP cmp_end_17
cmp_true_17:
    MOV t40, 1
cmp_end_17:
    CMP t40, 0
    JE L24    ; Saltar si falso
    ; return "C"
    MOV AX, 0
    RET
    JMP L22    ; Salto incondicional
L24:
    ; t41 = caracter EQ "d"
    MOV AX, caracter
    ; AL tiene el caracter
    CMP AL, 'd'
    JE cmp_true_18
    MOV t41, 0
    JMP cmp_end_18
cmp_true_18:
    MOV t41, 1
cmp_end_18:
    CMP t41, 0
    JE L25    ; Saltar si falso
    ; return "D"
    MOV AX, 0
    RET
    JMP L22    ; Salto incondicional
L25:
    ; t42 = caracter EQ "e"
    MOV AX, caracter
    ; AL tiene el caracter
    CMP AL, 'e'
    JE cmp_true_19
    MOV t42, 0
    JMP cmp_end_19
cmp_true_19:
    MOV t42, 1
cmp_end_19:
    CMP t42, 0
    JE L26    ; Saltar si falso
    ; return "E"
    MOV AX, 0
    RET
    JMP L22    ; Salto incondicional
L26:
    ; t43 = caracter EQ "f"
    MOV AX, caracter
    ; AL tiene el caracter
    CMP AL, 'f'
    JE cmp_true_20
    MOV t43, 0
    JMP cmp_end_20
cmp_true_20:
    MOV t43, 1
cmp_end_20:
    CMP t43, 0
    JE L27    ; Saltar si falso
    ; return "F"
    MOV AX, 0
    RET
    JMP L22    ; Salto incondicional
L27:
    ; t44 = caracter EQ "g"
    MOV AX, caracter
    ; AL tiene el caracter
    CMP AL, 'g'
    JE cmp_true_21
    MOV t44, 0
    JMP cmp_end_21
cmp_true_21:
    MOV t44, 1
cmp_end_21:
    CMP t44, 0
    JE L28    ; Saltar si falso
    ; return "G"
    MOV AX, 0
    RET
    JMP L22    ; Salto incondicional
L28:
    ; t45 = caracter EQ "h"
    MOV AX, caracter
    ; AL tiene el caracter
    CMP AL, 'h'
    JE cmp_true_22
    MOV t45, 0
    JMP cmp_end_22
cmp_true_22:
    MOV t45, 1
cmp_end_22:
    CMP t45, 0
    JE L29    ; Saltar si falso
    ; return "H"
    MOV AX, 0
    RET
    JMP L22    ; Salto incondicional
L29:
    ; t46 = caracter EQ "i"
    MOV AX, caracter
    ; AL tiene el caracter
    CMP AL, 'i'
    JE cmp_true_23
    MOV t46, 0
    JMP cmp_end_23
cmp_true_23:
    MOV t46, 1
cmp_end_23:
    CMP t46, 0
    JE L30    ; Saltar si falso
    ; return "I"
    MOV AX, 0
    RET
    JMP L22    ; Salto incondicional
L30:
    ; t47 = caracter EQ "j"
    MOV AX, caracter
    ; AL tiene el caracter
    CMP AL, 'j'
    JE cmp_true_24
    MOV t47, 0
    JMP cmp_end_24
cmp_true_24:
    MOV t47, 1
cmp_end_24:
    CMP t47, 0
    JE L31    ; Saltar si falso
    ; return "J"
    MOV AX, 0
    RET
    JMP L22    ; Salto incondicional
L31:
    ; t48 = caracter EQ "k"
    MOV AX, caracter
    ; AL tiene el caracter
    CMP AL, 'k'
    JE cmp_true_25
    MOV t48, 0
    JMP cmp_end_25
cmp_true_25:
    MOV t48, 1
cmp_end_25:
    CMP t48, 0
    JE L32    ; Saltar si falso
    ; return "K"
    MOV AX, 0
    RET
    JMP L22    ; Salto incondicional
L32:
    ; t49 = caracter EQ "l"
    MOV AX, caracter
    ; AL tiene el caracter
    CMP AL, 'l'
    JE cmp_true_26
    MOV t49, 0
    JMP cmp_end_26
cmp_true_26:
    MOV t49, 1
cmp_end_26:
    CMP t49, 0
    JE L33    ; Saltar si falso
    ; return "L"
    MOV AX, 0
    RET
    JMP L22    ; Salto incondicional
L33:
    ; t50 = caracter EQ "m"
    MOV AX, caracter
    ; AL tiene el caracter
    CMP AL, 'm'
    JE cmp_true_27
    MOV t50, 0
    JMP cmp_end_27
cmp_true_27:
    MOV t50, 1
cmp_end_27:
    CMP t50, 0
    JE L34    ; Saltar si falso
    ; return "M"
    MOV AX, 0
    RET
    JMP L22    ; Salto incondicional
L34:
    ; t51 = caracter EQ "n"
    MOV AX, caracter
    ; AL tiene el caracter
    CMP AL, 'n'
    JE cmp_true_28
    MOV t51, 0
    JMP cmp_end_28
cmp_true_28:
    MOV t51, 1
cmp_end_28:
    CMP t51, 0
    JE L35    ; Saltar si falso
    ; return "N"
    MOV AX, 0
    RET
    JMP L22    ; Salto incondicional
L35:
    ; t52 = caracter EQ "o"
    MOV AX, caracter
    ; AL tiene el caracter
    CMP AL, 'o'
    JE cmp_true_29
    MOV t52, 0
    JMP cmp_end_29
cmp_true_29:
    MOV t52, 1
cmp_end_29:
    CMP t52, 0
    JE L36    ; Saltar si falso
    ; return "O"
    MOV AX, 0
    RET
    JMP L22    ; Salto incondicional
L36:
    ; t53 = caracter EQ "p"
    MOV AX, caracter
    ; AL tiene el caracter
    CMP AL, 'p'
    JE cmp_true_30
    MOV t53, 0
    JMP cmp_end_30
cmp_true_30:
    MOV t53, 1
cmp_end_30:
    CMP t53, 0
    JE L37    ; Saltar si falso
    ; return "P"
    MOV AX, 0
    RET
    JMP L22    ; Salto incondicional
L37:
    ; t54 = caracter EQ "q"
    MOV AX, caracter
    ; AL tiene el caracter
    CMP AL, 'q'
    JE cmp_true_31
    MOV t54, 0
    JMP cmp_end_31
cmp_true_31:
    MOV t54, 1
cmp_end_31:
    CMP t54, 0
    JE L38    ; Saltar si falso
    ; return "Q"
    MOV AX, 0
    RET
    JMP L22    ; Salto incondicional
L38:
    ; t55 = caracter EQ "r"
    MOV AX, caracter
    ; AL tiene el caracter
    CMP AL, 'r'
    JE cmp_true_32
    MOV t55, 0
    JMP cmp_end_32
cmp_true_32:
    MOV t55, 1
cmp_end_32:
    CMP t55, 0
    JE L39    ; Saltar si falso
    ; return "R"
    MOV AX, 0
    RET
    JMP L22    ; Salto incondicional
L39:
    ; t56 = caracter EQ "s"
    MOV AX, caracter
    ; AL tiene el caracter
    CMP AL, 's'
    JE cmp_true_33
    MOV t56, 0
    JMP cmp_end_33
cmp_true_33:
    MOV t56, 1
cmp_end_33:
    CMP t56, 0
    JE L40    ; Saltar si falso
    ; return "S"
    MOV AX, 0
    RET
    JMP L22    ; Salto incondicional
L40:
    ; t57 = caracter EQ "t"
    MOV AX, caracter
    ; AL tiene el caracter
    CMP AL, 't'
    JE cmp_true_34
    MOV t57, 0
    JMP cmp_end_34
cmp_true_34:
    MOV t57, 1
cmp_end_34:
    CMP t57, 0
    JE L41    ; Saltar si falso
    ; return "T"
    MOV AX, 0
    RET
    JMP L22    ; Salto incondicional
L41:
    ; t58 = caracter EQ "u"
    MOV AX, caracter
    ; AL tiene el caracter
    CMP AL, 'u'
    JE cmp_true_35
    MOV t58, 0
    JMP cmp_end_35
cmp_true_35:
    MOV t58, 1
cmp_end_35:
    CMP t58, 0
    JE L42    ; Saltar si falso
    ; return "U"
    MOV AX, 0
    RET
    JMP L22    ; Salto incondicional
L42:
    ; t59 = caracter EQ "v"
    MOV AX, caracter
    ; AL tiene el caracter
    CMP AL, 'v'
    JE cmp_true_36
    MOV t59, 0
    JMP cmp_end_36
cmp_true_36:
    MOV t59, 1
cmp_end_36:
    CMP t59, 0
    JE L43    ; Saltar si falso
    ; return "V"
    MOV AX, 0
    RET
    JMP L22    ; Salto incondicional
L43:
    ; t60 = caracter EQ "w"
    MOV AX, caracter
    ; AL tiene el caracter
    CMP AL, 'w'
    JE cmp_true_37
    MOV t60, 0
    JMP cmp_end_37
cmp_true_37:
    MOV t60, 1
cmp_end_37:
    CMP t60, 0
    JE L44    ; Saltar si falso
    ; return "W"
    MOV AX, 0
    RET
    JMP L22    ; Salto incondicional
L44:
    ; t61 = caracter EQ "x"
    MOV AX, caracter
    ; AL tiene el caracter
    CMP AL, 'x'
    JE cmp_true_38
    MOV t61, 0
    JMP cmp_end_38
cmp_true_38:
    MOV t61, 1
cmp_end_38:
    CMP t61, 0
    JE L45    ; Saltar si falso
    ; return "X"
    MOV AX, 0
    RET
    JMP L22    ; Salto incondicional
L45:
    ; t62 = caracter EQ "y"
    MOV AX, caracter
    ; AL tiene el caracter
    CMP AL, 'y'
    JE cmp_true_39
    MOV t62, 0
    JMP cmp_end_39
cmp_true_39:
    MOV t62, 1
cmp_end_39:
    CMP t62, 0
    JE L46    ; Saltar si falso
    ; return "Y"
    MOV AX, 0
    RET
    JMP L22    ; Salto incondicional
L46:
    ; t63 = caracter EQ "z"
    MOV AX, caracter
    ; AL tiene el caracter
    CMP AL, 'z'
    JE cmp_true_40
    MOV t63, 0
    JMP cmp_end_40
cmp_true_40:
    MOV t63, 1
cmp_end_40:
    CMP t63, 0
    JE L47    ; Saltar si falso
    ; return "Z"
    MOV AX, 0
    RET
    JMP L22    ; Salto incondicional
L47:
    MOV AX, caracter    ; Cargar caracter
    ; return caracter
    RET
L22:
    ; return None
    MOV AX, 0
    RET
convertir_a_mayuscula ENDP

; ---------------------------------------------------------
; Función: a_mayusculas
; ---------------------------------------------------------
a_mayusculas PROC
    ; resultado = ""
    ; i = 0
    MOV BX, 0    ; Cargar constante 0
    MOV i, BX    ; Almacenar en i
L48:
    ; t64 = len()
    MOV AX, texto_len    ; len(texto)
    MOV t64, AX
    ; t65 = i LT t64
    MOV CX, i    ; Cargar i
    MOV DX, t64    ; Cargar t64
    MOV SI, 0    ; Inicializar resultado
    CMP CX, DX
    JL L41_true
    JMP L41_end
L41_true:
    MOV SI, 1
L41_end:
    MOV t65, SI    ; Almacenar en t65
    CMP t65, 0
    JE L49    ; Saltar si falso
    ; t66 = texto[i]
    MOV BX, texto
    ADD BX, i
    MOV AL, [BX]    ; AL tiene el caracter
    MOV AH, 0
    MOV t66, AX ; Guardar en t66
    ; ch = t66
    MOV DI, t66    ; Cargar t66
    MOV ch, DI    ; Almacenar en ch
    ; t67 = convertir_a_mayuscula()
    ; Guardar registros antes de llamar función
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    MOV AX, ch    ; Cargar ch
    MOV caracter, AX
    CALL convertir_a_mayuscula
    POP DX
    POP CX
    POP BX
    POP AX
    MOV BX, AX
    MOV t67, BX    ; Almacenar en t67
    ; mayus = t67
    MOV CX, t67    ; Cargar t67
    MOV mayus, CX    ; Almacenar en mayus
    ; t68 = resultado + mayus
    MOV SI, resultado    ; Cargar resultado
    MOV DI, mayus    ; Cargar mayus
    MOV AX, SI
    ADD AX, DI
    MOV t68, AX
    ; t69 = i + 1
    MOV BX, i    ; Cargar i
    MOV CX, 1    ; Cargar constante 1
    MOV DX, BX
    ADD DX, CX
    MOV t69, DX
    ; i = t69
    MOV SI, t69    ; Cargar t69
    MOV i, SI    ; Almacenar en i
    JMP L48    ; Salto incondicional
L49:
    MOV DI, resultado    ; Cargar resultado
    ; return resultado
    MOV AX, DI
    RET
a_mayusculas ENDP

; ---------------------------------------------------------
; Función: menu
; ---------------------------------------------------------
menu PROC
    ; opcion = ""
L50:
    ; t70 = opcion NEQ "6"
    MOV AX, opcion
    ; AL tiene el caracter
    CMP AL, '6'
    JNE cmp_true_42
    MOV t70, 0
    JMP cmp_end_42
cmp_true_42:
    MOV t70, 1
cmp_end_42:
    CMP t70, 0
    JE L51    ; Saltar si falso
    ; print("
===== PROCESAMIENTO DE CADENAS =====")
    MOV DX, OFFSET str_0
    MOV AH, 09h
    INT 21h
    ; print("1. Contar vocales")
    MOV DX, OFFSET str_1
    MOV AH, 09h
    INT 21h
    ; print("2. Invertir cadena")
    MOV DX, OFFSET str_2
    MOV AH, 09h
    INT 21h
    ; print("3. Verificar palíndromo")
    MOV DX, OFFSET str_3
    MOV AH, 09h
    INT 21h
    ; print("4. Contar un carácter específico")
    MOV DX, OFFSET str_4
    MOV AH, 09h
    INT 21h
    ; print("5. Convertir a mayúsculas")
    MOV DX, OFFSET str_5
    MOV AH, 09h
    INT 21h
    ; print("6. Salir")
    MOV DX, OFFSET str_6
    MOV AH, 09h
    INT 21h
    ; pedir número
    MOV DX, OFFSET str_7
    MOV AH, 09h
    INT 21h
    ; leer número
    MOV DX, OFFSET t71
    MOV AH, 0Ah
    INT 21h
    ; preparar cadena
    MOV SI, OFFSET t71+2
    MOV CL, [t71+1]
    ADD SI, CX
    MOV BYTE PTR [SI], 0
    MOV SI, OFFSET t71+2
    ; opcion = t71
    MOV AX, t71    ; Cargar t71
    MOV opcion, AX    ; Almacenar en opcion
    ; t72 = opcion EQ "1"
    MOV AX, opcion
    ; AL tiene el caracter
    CMP AL, '1'
    JE cmp_true_43
    MOV t72, 0
    JMP cmp_end_43
cmp_true_43:
    MOV t72, 1
cmp_end_43:
    CMP t72, 0
    JE L52    ; Saltar si falso
    ; pedir número
    MOV DX, OFFSET str_8
    MOV AH, 09h
    INT 21h
    ; leer número
    MOV DX, OFFSET t73
    MOV AH, 0Ah
    INT 21h
    ; preparar cadena
    MOV SI, OFFSET t73+2
    MOV CL, [t73+1]
    ADD SI, CX
    MOV BYTE PTR [SI], 0
    MOV SI, OFFSET t73+2
    ; texto = t73
    MOV CX, t73    ; Cargar t73
    MOV texto, CX    ; Almacenar en texto
    ; print("Cantidad de vocales:")
    MOV DX, OFFSET str_9
    MOV AH, 09h
    INT 21h
    ; t74 = contar_vocales()
    ; Guardar registros antes de llamar función
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    MOV SI, texto    ; Cargar texto
    MOV texto, SI
    CALL contar_vocales
    POP DX
    POP CX
    POP BX
    POP AX
    MOV DI, AX
    MOV t74, DI    ; Almacenar en t74
    MOV AX, t74
    CALL print_number_inline
    JMP L53    ; Salto incondicional
L52:
    ; t75 = opcion EQ "2"
    MOV AX, opcion
    ; AL tiene el caracter
    CMP AL, '2'
    JE cmp_true_44
    MOV t75, 0
    JMP cmp_end_44
cmp_true_44:
    MOV t75, 1
cmp_end_44:
    CMP t75, 0
    JE L54    ; Saltar si falso
    ; pedir número
    MOV DX, OFFSET str_8
    MOV AH, 09h
    INT 21h
    ; leer número
    MOV DX, OFFSET t76
    MOV AH, 0Ah
    INT 21h
    ; preparar cadena
    MOV SI, OFFSET t76+2
    MOV CL, [t76+1]
    ADD SI, CX
    MOV BYTE PTR [SI], 0
    MOV SI, OFFSET t76+2
    ; texto = t76
    MOV AX, t76    ; Cargar t76
    MOV texto, AX    ; Almacenar en texto
    ; print("Invertida:")
    MOV DX, OFFSET str_10
    MOV AH, 09h
    INT 21h
    ; t77 = invertir()
    ; Guardar registros antes de llamar función
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    MOV BX, texto    ; Cargar texto
    MOV texto, BX
    CALL invertir
    POP DX
    POP CX
    POP BX
    POP AX
    MOV CX, AX
    MOV t77, CX    ; Almacenar en t77
    MOV AX, t77
    CALL print_number_inline
    JMP L53    ; Salto incondicional
L54:
    ; t78 = opcion EQ "3"
    MOV AX, opcion
    ; AL tiene el caracter
    CMP AL, '3'
    JE cmp_true_45
    MOV t78, 0
    JMP cmp_end_45
cmp_true_45:
    MOV t78, 1
cmp_end_45:
    CMP t78, 0
    JE L55    ; Saltar si falso
    ; pedir número
    MOV DX, OFFSET str_8
    MOV AH, 09h
    INT 21h
    ; leer número
    MOV DX, OFFSET t79
    MOV AH, 0Ah
    INT 21h
    ; preparar cadena
    MOV SI, OFFSET t79+2
    MOV CL, [t79+1]
    ADD SI, CX
    MOV BYTE PTR [SI], 0
    MOV SI, OFFSET t79+2
    ; texto = t79
    MOV DX, t79    ; Cargar t79
    MOV texto, DX    ; Almacenar en texto
    ; t80 = es_palindromo()
    ; Guardar registros antes de llamar función
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    MOV SI, texto    ; Cargar texto
    MOV texto, SI
    CALL es_palindromo
    POP DX
    POP CX
    POP BX
    POP AX
    MOV DI, AX
    MOV t80, DI    ; Almacenar en t80
    CMP t80, 0
    JE L56    ; Saltar si falso
    ; print(" Es palíndromo.")
    MOV DX, OFFSET str_11
    MOV AH, 09h
    INT 21h
    JMP L57    ; Salto incondicional
L56:
    ; print(" No es palíndromo.")
    MOV DX, OFFSET str_12
    MOV AH, 09h
    INT 21h
L57:
    JMP L53    ; Salto incondicional
L55:
    ; t81 = opcion EQ "4"
    MOV AX, opcion
    ; AL tiene el caracter
    CMP AL, '4'
    JE cmp_true_46
    MOV t81, 0
    JMP cmp_end_46
cmp_true_46:
    MOV t81, 1
cmp_end_46:
    CMP t81, 0
    JE L58    ; Saltar si falso
    ; pedir número
    MOV DX, OFFSET str_8
    MOV AH, 09h
    INT 21h
    ; leer número
    MOV DX, OFFSET t82
    MOV AH, 0Ah
    INT 21h
    ; preparar cadena
    MOV SI, OFFSET t82+2
    MOV CL, [t82+1]
    ADD SI, CX
    MOV BYTE PTR [SI], 0
    MOV SI, OFFSET t82+2
    ; texto = t82
    MOV AX, t82    ; Cargar t82
    MOV texto, AX    ; Almacenar en texto
    ; pedir número
    MOV DX, OFFSET str_13
    MOV AH, 09h
    INT 21h
    ; leer número
    MOV DX, OFFSET t83
    MOV AH, 0Ah
    INT 21h
    ; preparar cadena
    MOV SI, OFFSET t83+2
    MOV CL, [t83+1]
    ADD SI, CX
    MOV BYTE PTR [SI], 0
    MOV SI, OFFSET t83+2
    ; caracter = t83
    MOV BX, t83    ; Cargar t83
    MOV caracter, BX    ; Almacenar en caracter
    ; print("El carácter aparece")
    MOV DX, OFFSET str_14
    MOV AH, 09h
    INT 21h
    ; t84 = contar_caracter()
    ; Guardar registros antes de llamar función
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    MOV DX, texto    ; Cargar texto
    MOV texto, DX
    MOV SI, caracter    ; Cargar caracter
    MOV caracter, SI
    CALL contar_caracter
    POP DX
    POP CX
    POP BX
    POP AX
    MOV DI, AX
    MOV t84, DI    ; Almacenar en t84
    MOV AX, t84
    CALL print_number_inline
    ; print("veces.")
    MOV DX, OFFSET str_15
    MOV AH, 09h
    INT 21h
    JMP L53    ; Salto incondicional
L58:
    ; t85 = opcion EQ "5"
    MOV AX, opcion
    ; AL tiene el caracter
    CMP AL, '5'
    JE cmp_true_47
    MOV t85, 0
    JMP cmp_end_47
cmp_true_47:
    MOV t85, 1
cmp_end_47:
    CMP t85, 0
    JE L59    ; Saltar si falso
    ; pedir número
    MOV DX, OFFSET str_8
    MOV AH, 09h
    INT 21h
    ; leer número
    MOV DX, OFFSET t86
    MOV AH, 0Ah
    INT 21h
    ; preparar cadena
    MOV SI, OFFSET t86+2
    MOV CL, [t86+1]
    ADD SI, CX
    MOV BYTE PTR [SI], 0
    MOV SI, OFFSET t86+2
    ; texto = t86
    MOV AX, t86    ; Cargar t86
    MOV texto, AX    ; Almacenar en texto
    ; print("En mayúsculas:")
    MOV DX, OFFSET str_16
    MOV AH, 09h
    INT 21h
    ; t87 = a_mayusculas()
    ; Guardar registros antes de llamar función
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    MOV BX, texto    ; Cargar texto
    MOV texto, BX
    CALL a_mayusculas
    POP DX
    POP CX
    POP BX
    POP AX
    MOV CX, AX
    MOV t87, CX    ; Almacenar en t87
    MOV AX, t87
    CALL print_number_inline
    JMP L53    ; Salto incondicional
L59:
    ; t88 = opcion EQ "6"
    MOV AX, opcion
    ; AL tiene el caracter
    CMP AL, '6'
    JE cmp_true_48
    MOV t88, 0
    JMP cmp_end_48
cmp_true_48:
    MOV t88, 1
cmp_end_48:
    CMP t88, 0
    JE L60    ; Saltar si falso
    ; print(" Saliendo...")
    MOV DX, OFFSET str_17
    MOV AH, 09h
    INT 21h
    JMP L53    ; Salto incondicional
L60:
    ; print(" Opción inválida.")
    MOV DX, OFFSET str_18
    MOV AH, 09h
    INT 21h
L53:
    JMP L50    ; Salto incondicional
L51:
    ; return None
    MOV AX, 0
    RET
menu ENDP

; ---------------------------------------------------------
; Función: main
; ---------------------------------------------------------
user_main PROC
    ; t89 = menu()
    ; Guardar registros antes de llamar función
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    CALL menu
    POP DX
    POP CX
    POP BX
    POP AX
    MOV DX, AX
    MOV t89, DX    ; Almacenar en t89
    ; return None
    MOV AX, 0
    RET
    ; t90 = main()
    ; Guardar registros antes de llamar función
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    CALL user_main
    POP DX
    POP CX
    POP BX
    POP AX
    MOV SI, AX
    MOV t90, SI    ; Almacenar en t90
user_main ENDP

; Función: contar_vocales
contar_vocales PROC
    ; contador = 0
    MOV DI, 0    ; Cargar constante 0
    MOV contador, DI    ; Almacenar en contador
    ; i = 0
    MOV AX, 0    ; Cargar constante 0
    MOV i, AX    ; Almacenar en i
L0:
    ; t0 = len()
    MOV AX, texto_len    ; len(texto)
    MOV t0, AX
    ; t1 = i LT t0
    MOV BX, i    ; Cargar i
    MOV CX, t0    ; Cargar t0
    MOV AX, 0    ; Inicializar resultado
    CMP BX, CX
    JL L49_true
    JMP L49_end
L49_true:
    MOV AX, 1
L49_end:
    MOV t1, AX    ; Almacenar en t1
    CMP t1, 0
    JE L1    ; Saltar si falso
    ; t2 = texto[i]
    MOV BX, texto
    ADD BX, i
    MOV AL, [BX]    ; AL tiene el caracter
    MOV AH, 0
    MOV t2, AX ; Guardar en t2
    ; ch = t2
    MOV DX, t2    ; Cargar t2
    MOV ch, DX    ; Almacenar en ch
    ; t3 = ch EQ "a"
    MOV AX, ch
    ; AL tiene el caracter
    CMP AL, 'a'
    JE cmp_true_50
    MOV t3, 0
    JMP cmp_end_50
cmp_true_50:
    MOV t3, 1
cmp_end_50:
    CMP t3, 0
    JE L2    ; Saltar si falso
    ; t4 = contador + 1
    MOV SI, contador    ; Cargar contador
    MOV DI, 1    ; Cargar constante 1
    MOV DI, SI
    ADD DI, DI
    MOV t4, DI
    JMP L3    ; Salto incondicional
L2:
    ; t5 = ch EQ "e"
    MOV AX, ch
    ; AL tiene el caracter
    CMP AL, 'e'
    JE cmp_true_51
    MOV t5, 0
    JMP cmp_end_51
cmp_true_51:
    MOV t5, 1
cmp_end_51:
    CMP t5, 0
    JE L4    ; Saltar si falso
    ; t6 = contador + 1
    MOV AX, contador    ; Cargar contador
    MOV BX, 1    ; Cargar constante 1
    MOV CX, AX
    ADD CX, BX
    MOV t6, CX
    ; contador = t6
    MOV CX, t6    ; Cargar t6
    MOV contador, CX    ; Almacenar en contador
    JMP L3    ; Salto incondicional
L4:
    ; t7 = ch EQ "i"
    MOV AX, ch
    ; AL tiene el caracter
    CMP AL, 'i'
    JE cmp_true_52
    MOV t7, 0
    JMP cmp_end_52
cmp_true_52:
    MOV t7, 1
cmp_end_52:
    CMP t7, 0
    JE L5    ; Saltar si falso
    ; t8 = contador + 1
    MOV DX, contador    ; Cargar contador
    MOV SI, 1    ; Cargar constante 1
    MOV AX, DX
    ADD AX, SI
    MOV t8, AX
    ; contador = t8
    MOV DI, t8    ; Cargar t8
    MOV contador, DI    ; Almacenar en contador
    JMP L3    ; Salto incondicional
L5:
    ; t9 = ch EQ "o"
    MOV AX, ch
    ; AL tiene el caracter
    CMP AL, 'o'
    JE cmp_true_53
    MOV t9, 0
    JMP cmp_end_53
cmp_true_53:
    MOV t9, 1
cmp_end_53:
    CMP t9, 0
    JE L6    ; Saltar si falso
    ; t10 = contador + 1
    MOV AX, contador    ; Cargar contador
    MOV BX, 1    ; Cargar constante 1
    MOV SI, AX
    ADD SI, BX
    MOV t10, SI
    ; contador = t10
    MOV CX, t10    ; Cargar t10
    MOV contador, CX    ; Almacenar en contador
    JMP L3    ; Salto incondicional
L6:
    ; t11 = ch EQ "u"
    MOV AX, ch
    ; AL tiene el caracter
    CMP AL, 'u'
    JE cmp_true_54
    MOV t11, 0
    JMP cmp_end_54
cmp_true_54:
    MOV t11, 1
cmp_end_54:
    CMP t11, 0
    JE L7    ; Saltar si falso
    ; t12 = contador + 1
    MOV DX, contador    ; Cargar contador
    MOV SI, 1    ; Cargar constante 1
    MOV CX, DX
    ADD CX, SI
    MOV t12, CX
    ; contador = t12
    MOV DI, t12    ; Cargar t12
    MOV contador, DI    ; Almacenar en contador
    JMP L3    ; Salto incondicional
L7:
    ; t13 = ch EQ "A"
    MOV AX, ch
    ; AL tiene el caracter
    CMP AL, 'A'
    JE cmp_true_55
    MOV t13, 0
    JMP cmp_end_55
cmp_true_55:
    MOV t13, 1
cmp_end_55:
    CMP t13, 0
    JE L8    ; Saltar si falso
    ; t14 = contador + 1
    MOV AX, contador    ; Cargar contador
    MOV BX, 1    ; Cargar constante 1
    MOV AX, AX
    ADD AX, BX
    MOV t14, AX
    ; contador = t14
    MOV CX, t14    ; Cargar t14
    MOV contador, CX    ; Almacenar en contador
    JMP L3    ; Salto incondicional
L8:
    ; t15 = ch EQ "E"
    MOV AX, ch
    ; AL tiene el caracter
    CMP AL, 'E'
    JE cmp_true_56
    MOV t15, 0
    JMP cmp_end_56
cmp_true_56:
    MOV t15, 1
cmp_end_56:
    CMP t15, 0
    JE L9    ; Saltar si falso
    ; t16 = contador + 1
    MOV DX, contador    ; Cargar contador
    MOV SI, 1    ; Cargar constante 1
    MOV SI, DX
    ADD SI, SI
    MOV t16, SI
    ; contador = t16
    MOV DI, t16    ; Cargar t16
    MOV contador, DI    ; Almacenar en contador
    JMP L3    ; Salto incondicional
L9:
    ; t17 = ch EQ "I"
    MOV AX, ch
    ; AL tiene el caracter
    CMP AL, 'I'
    JE cmp_true_57
    MOV t17, 0
    JMP cmp_end_57
cmp_true_57:
    MOV t17, 1
cmp_end_57:
    CMP t17, 0
    JE L10    ; Saltar si falso
    ; t18 = contador + 1
    MOV AX, contador    ; Cargar contador
    MOV BX, 1    ; Cargar constante 1
    MOV CX, AX
    ADD CX, BX
    MOV t18, CX
    ; contador = t18
    MOV CX, t18    ; Cargar t18
    MOV contador, CX    ; Almacenar en contador
    JMP L3    ; Salto incondicional
L10:
    ; t19 = ch EQ "O"
    MOV AX, ch
    ; AL tiene el caracter
    CMP AL, 'O'
    JE cmp_true_58
    MOV t19, 0
    JMP cmp_end_58
cmp_true_58:
    MOV t19, 1
cmp_end_58:
    CMP t19, 0
    JE L11    ; Saltar si falso
    ; t20 = contador + 1
    MOV DX, contador    ; Cargar contador
    MOV SI, 1    ; Cargar constante 1
    MOV AX, DX
    ADD AX, SI
    MOV t20, AX
    ; contador = t20
    MOV DI, t20    ; Cargar t20
    MOV contador, DI    ; Almacenar en contador
    JMP L3    ; Salto incondicional
L11:
    ; t21 = ch EQ "U"
    MOV AX, ch
    ; AL tiene el caracter
    CMP AL, 'U'
    JE cmp_true_59
    MOV t21, 0
    JMP cmp_end_59
cmp_true_59:
    MOV t21, 1
cmp_end_59:
    CMP t21, 0
    JE L12    ; Saltar si falso
    ; t22 = contador + 1
    MOV AX, contador    ; Cargar contador
    MOV BX, 1    ; Cargar constante 1
    MOV SI, AX
    ADD SI, BX
    MOV t22, SI
    ; contador = t22
    MOV CX, t22    ; Cargar t22
    MOV contador, CX    ; Almacenar en contador
    JMP L3    ; Salto incondicional
L12:
L3:
    ; t23 = i + 1
    MOV DX, i    ; Cargar i
    MOV SI, 1    ; Cargar constante 1
    MOV CX, DX
    ADD CX, SI
    MOV t23, CX
    ; i = t23
    MOV DI, t23    ; Cargar t23
    MOV i, DI    ; Almacenar en i
    JMP L0    ; Salto incondicional
L1:
    MOV AX, contador    ; Cargar contador
    ; return contador
    RET
contar_vocales ENDP

; Función: invertir
invertir PROC
    ; invertida = ""
    ; t24 = len()
    MOV AX, texto_len    ; len(texto)
    MOV t24, AX
    ; t25 = t24 - 1
    MOV BX, t24    ; Cargar t24
    MOV CX, 1    ; Cargar constante 1
    MOV BX, BX
    SUB BX, CX
    MOV t25, BX    ; Almacenar en t25
    ; i = t25
    MOV DX, t25    ; Cargar t25
    MOV i, DX    ; Almacenar en i
L13:
    ; t26 = i GTE 0
    MOV SI, i    ; Cargar i
    MOV DI, 0    ; Cargar constante 0
    MOV DI, 0    ; Inicializar resultado
    CMP SI, DI
    JGE L60_true
    JMP L60_end
L60_true:
    MOV DI, 1
L60_end:
    MOV t26, DI    ; Almacenar en t26
    CMP t26, 0
    JE L14    ; Saltar si falso
    ; t27 = texto[i]
    MOV BX, texto
    ADD BX, i
    MOV AL, [BX]    ; AL tiene el caracter
    MOV AH, 0
    MOV t27, AX ; Guardar en t27
    ; t28 = invertida + t27
    MOV AX, invertida    ; Cargar invertida
    MOV BX, t27    ; Cargar t27
    MOV CX, AX
    ADD CX, BX
    MOV t28, CX
    ; invertida = t28
    MOV CX, t28    ; Cargar t28
    MOV invertida, CX    ; Almacenar en invertida
    ; t29 = i - 1
    MOV DX, i    ; Cargar i
    MOV SI, 1    ; Cargar constante 1
    MOV BX, DX
    SUB BX, SI
    MOV t29, BX    ; Almacenar en t29
    ; i = t29
    MOV DI, t29    ; Cargar t29
    MOV i, DI    ; Almacenar en i
    JMP L13    ; Salto incondicional
L14:
    MOV AX, invertida    ; Cargar invertida
    ; return invertida
    RET
invertir ENDP

; Función: es_palindromo
es_palindromo PROC
    ; t30 = invertir()
    ; Guardar registros antes de llamar función
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    MOV BX, texto    ; Cargar texto
    MOV texto, BX
    CALL invertir
    POP DX
    POP CX
    POP BX
    POP AX
    MOV DI, AX
    MOV t30, DI    ; Almacenar en t30
    ; texto_invertido = t30
    MOV CX, t30    ; Cargar t30
    MOV texto_invertido, CX    ; Almacenar en texto_invertido
    ; t31 = texto_invertido EQ texto
    MOV DX, texto_invertido    ; Cargar texto_invertido
    MOV SI, texto    ; Cargar texto
    MOV SI, 0    ; Inicializar resultado
    CMP DX, SI
    JE L61_true
    JMP L61_end
L61_true:
    MOV SI, 1
L61_end:
    MOV t31, SI    ; Almacenar en t31
    CMP t31, 0
    JE L15    ; Saltar si falso
    MOV DI, 1    ; Cargar constante 1
    ; return 1
    MOV AX, DI
    RET
es_palindromo ENDP

; Función: contar_caracter
contar_caracter PROC
    ; contador = 0
    MOV AX, 0    ; Cargar constante 0
    MOV contador, AX    ; Almacenar en contador
    ; i = 0
    MOV BX, 0    ; Cargar constante 0
    MOV i, BX    ; Almacenar en i
L17:
    ; t32 = len()
    MOV AX, texto_len    ; len(texto)
    MOV t32, AX
    ; t33 = i LT t32
    MOV CX, i    ; Cargar i
    MOV DX, t32    ; Cargar t32
    MOV DI, 0    ; Inicializar resultado
    CMP CX, DX
    JL L62_true
    JMP L62_end
L62_true:
    MOV DI, 1
L62_end:
    MOV t33, DI    ; Almacenar en t33
    CMP t33, 0
    JE L18    ; Saltar si falso
    ; t34 = texto[i]
    MOV BX, texto
    ADD BX, i
    MOV AL, [BX]    ; AL tiene el caracter
    MOV AH, 0
    MOV t34, AX ; Guardar en t34
    ; t35 = t34 EQ caracter
    MOV SI, t34    ; Cargar t34
    MOV DI, caracter    ; Cargar caracter
    MOV CX, 0    ; Inicializar resultado
    CMP SI, DI
    JE L63_true
    JMP L63_end
L63_true:
    MOV CX, 1
L63_end:
    MOV t35, CX    ; Almacenar en t35
    CMP t35, 0
    JE L19    ; Saltar si falso
    ; t36 = contador + 1
    MOV AX, contador    ; Cargar contador
    MOV BX, 1    ; Cargar constante 1
    MOV DI, AX
    ADD DI, BX
    MOV t36, DI
    ; contador = t36
    MOV CX, t36    ; Cargar t36
    MOV contador, CX    ; Almacenar en contador
    JMP L20    ; Salto incondicional
L19:
L20:
    ; t37 = i + 1
    MOV DX, i    ; Cargar i
    MOV SI, 1    ; Cargar constante 1
    MOV DX, DX
    ADD DX, SI
    MOV t37, DX
    ; i = t37
    MOV DI, t37    ; Cargar t37
    MOV i, DI    ; Almacenar en i
    JMP L17    ; Salto incondicional
L18:
    MOV AX, contador    ; Cargar contador
    ; return contador
    RET
contar_caracter ENDP

; Función: convertir_a_mayuscula
convertir_a_mayuscula PROC
    ; t38 = caracter EQ "a"
    MOV AX, caracter
    ; AL tiene el caracter
    CMP AL, 'a'
    JE cmp_true_64
    MOV t38, 0
    JMP cmp_end_64
cmp_true_64:
    MOV t38, 1
cmp_end_64:
    CMP t38, 0
    JE L21    ; Saltar si falso
    ; return "A"
    MOV AX, 0
    RET
convertir_a_mayuscula ENDP

; Función: a_mayusculas
a_mayusculas PROC
    ; resultado = ""
    ; i = 0
    MOV BX, 0    ; Cargar constante 0
    MOV i, BX    ; Almacenar en i
L48:
    ; t64 = len()
    MOV AX, texto_len    ; len(texto)
    MOV t64, AX
    ; t65 = i LT t64
    MOV CX, i    ; Cargar i
    MOV DX, t64    ; Cargar t64
    MOV SI, 0    ; Inicializar resultado
    CMP CX, DX
    JL L65_true
    JMP L65_end
L65_true:
    MOV SI, 1
L65_end:
    MOV t65, SI    ; Almacenar en t65
    CMP t65, 0
    JE L49    ; Saltar si falso
    ; t66 = texto[i]
    MOV BX, texto
    ADD BX, i
    MOV AL, [BX]    ; AL tiene el caracter
    MOV AH, 0
    MOV t66, AX ; Guardar en t66
    ; ch = t66
    MOV SI, t66    ; Cargar t66
    MOV ch, SI    ; Almacenar en ch
    ; t67 = convertir_a_mayuscula()
    ; Guardar registros antes de llamar función
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    MOV DI, ch    ; Cargar ch
    MOV caracter, DI
    CALL convertir_a_mayuscula
    POP DX
    POP CX
    POP BX
    POP AX
    MOV BX, AX
    MOV t67, BX    ; Almacenar en t67
    ; mayus = t67
    MOV AX, t67    ; Cargar t67
    MOV mayus, AX    ; Almacenar en mayus
    ; t68 = resultado + mayus
    MOV BX, resultado    ; Cargar resultado
    MOV CX, mayus    ; Cargar mayus
    MOV AX, BX
    ADD AX, CX
    MOV t68, AX
    ; t69 = i + 1
    MOV DX, i    ; Cargar i
    MOV SI, 1    ; Cargar constante 1
    MOV DX, DX
    ADD DX, SI
    MOV t69, DX
    ; i = t69
    MOV DI, t69    ; Cargar t69
    MOV i, DI    ; Almacenar en i
    JMP L48    ; Salto incondicional
L49:
    MOV AX, resultado    ; Cargar resultado
    ; return resultado
    RET
a_mayusculas ENDP

; Función: menu
menu PROC
    ; opcion = ""
L50:
    ; t70 = opcion NEQ "6"
    MOV AX, opcion
    ; AL tiene el caracter
    CMP AL, '6'
    JNE cmp_true_66
    MOV t70, 0
    JMP cmp_end_66
cmp_true_66:
    MOV t70, 1
cmp_end_66:
    CMP t70, 0
    JE L51    ; Saltar si falso
    ; print("
===== PROCESAMIENTO DE CADENAS =====")
    MOV DX, OFFSET str_0
    MOV AH, 09h
    INT 21h
    ; print("1. Contar vocales")
    MOV DX, OFFSET str_1
    MOV AH, 09h
    INT 21h
    ; print("2. Invertir cadena")
    MOV DX, OFFSET str_2
    MOV AH, 09h
    INT 21h
    ; print("3. Verificar palíndromo")
    MOV DX, OFFSET str_3
    MOV AH, 09h
    INT 21h
    ; print("4. Contar un carácter específico")
    MOV DX, OFFSET str_4
    MOV AH, 09h
    INT 21h
    ; print("5. Convertir a mayúsculas")
    MOV DX, OFFSET str_5
    MOV AH, 09h
    INT 21h
    ; print("6. Salir")
    MOV DX, OFFSET str_6
    MOV AH, 09h
    INT 21h
    ; pedir número
    MOV DX, OFFSET str_7
    MOV AH, 09h
    INT 21h
    ; leer número
    MOV DX, OFFSET t71
    MOV AH, 0Ah
    INT 21h
    ; preparar cadena
    MOV SI, OFFSET t71+2
    MOV CL, [t71+1]
    ADD SI, CX
    MOV BYTE PTR [SI], 0
    MOV SI, OFFSET t71+2
    ; opcion = t71
    MOV BX, t71    ; Cargar t71
    MOV opcion, BX    ; Almacenar en opcion
    ; t72 = opcion EQ "1"
    MOV AX, opcion
    ; AL tiene el caracter
    CMP AL, '1'
    JE cmp_true_67
    MOV t72, 0
    JMP cmp_end_67
cmp_true_67:
    MOV t72, 1
cmp_end_67:
    CMP t72, 0
    JE L52    ; Saltar si falso
    ; pedir número
    MOV DX, OFFSET str_8
    MOV AH, 09h
    INT 21h
    ; leer número
    MOV DX, OFFSET t73
    MOV AH, 0Ah
    INT 21h
    ; preparar cadena
    MOV SI, OFFSET t73+2
    MOV CL, [t73+1]
    ADD SI, CX
    MOV BYTE PTR [SI], 0
    MOV SI, OFFSET t73+2
    ; texto = t73
    MOV CX, t73    ; Cargar t73
    MOV texto, CX    ; Almacenar en texto
    ; print("Cantidad de vocales:")
    MOV DX, OFFSET str_9
    MOV AH, 09h
    INT 21h
    ; t74 = contar_vocales()
    ; Guardar registros antes de llamar función
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    MOV DX, texto    ; Cargar texto
    MOV texto, DX
    CALL contar_vocales
    POP DX
    POP CX
    POP BX
    POP AX
    MOV DI, AX
    MOV t74, DI    ; Almacenar en t74
    MOV AX, t74
    CALL print_number_inline
    JMP L53    ; Salto incondicional
L52:
    ; t75 = opcion EQ "2"
    MOV AX, opcion
    ; AL tiene el caracter
    CMP AL, '2'
    JE cmp_true_68
    MOV t75, 0
    JMP cmp_end_68
cmp_true_68:
    MOV t75, 1
cmp_end_68:
    CMP t75, 0
    JE L54    ; Saltar si falso
    ; pedir número
    MOV DX, OFFSET str_8
    MOV AH, 09h
    INT 21h
    ; leer número
    MOV DX, OFFSET t76
    MOV AH, 0Ah
    INT 21h
    ; preparar cadena
    MOV SI, OFFSET t76+2
    MOV CL, [t76+1]
    ADD SI, CX
    MOV BYTE PTR [SI], 0
    MOV SI, OFFSET t76+2
    ; texto = t76
    MOV SI, t76    ; Cargar t76
    MOV texto, SI    ; Almacenar en texto
    ; print("Invertida:")
    MOV DX, OFFSET str_10
    MOV AH, 09h
    INT 21h
    ; t77 = invertir()
    ; Guardar registros antes de llamar función
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    MOV DI, texto    ; Cargar texto
    MOV texto, DI
    CALL invertir
    POP DX
    POP CX
    POP BX
    POP AX
    MOV CX, AX
    MOV t77, CX    ; Almacenar en t77
    MOV AX, t77
    CALL print_number_inline
    JMP L53    ; Salto incondicional
L54:
    ; t78 = opcion EQ "3"
    MOV AX, opcion
    ; AL tiene el caracter
    CMP AL, '3'
    JE cmp_true_69
    MOV t78, 0
    JMP cmp_end_69
cmp_true_69:
    MOV t78, 1
cmp_end_69:
    CMP t78, 0
    JE L55    ; Saltar si falso
    ; pedir número
    MOV DX, OFFSET str_8
    MOV AH, 09h
    INT 21h
    ; leer número
    MOV DX, OFFSET t79
    MOV AH, 0Ah
    INT 21h
    ; preparar cadena
    MOV SI, OFFSET t79+2
    MOV CL, [t79+1]
    ADD SI, CX
    MOV BYTE PTR [SI], 0
    MOV SI, OFFSET t79+2
    ; texto = t79
    MOV AX, t79    ; Cargar t79
    MOV texto, AX    ; Almacenar en texto
    ; t80 = es_palindromo()
    ; Guardar registros antes de llamar función
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    MOV BX, texto    ; Cargar texto
    MOV texto, BX
    CALL es_palindromo
    POP DX
    POP CX
    POP BX
    POP AX
    MOV DI, AX
    MOV t80, DI    ; Almacenar en t80
    CMP t80, 0
    JE L56    ; Saltar si falso
    ; print(" Es palíndromo.")
    MOV DX, OFFSET str_11
    MOV AH, 09h
    INT 21h
    JMP L57    ; Salto incondicional
L56:
    ; print(" No es palíndromo.")
    MOV DX, OFFSET str_12
    MOV AH, 09h
    INT 21h
L57:
    JMP L53    ; Salto incondicional
L55:
    ; t81 = opcion EQ "4"
    MOV AX, opcion
    ; AL tiene el caracter
    CMP AL, '4'
    JE cmp_true_70
    MOV t81, 0
    JMP cmp_end_70
cmp_true_70:
    MOV t81, 1
cmp_end_70:
    CMP t81, 0
    JE L58    ; Saltar si falso
    ; pedir número
    MOV DX, OFFSET str_8
    MOV AH, 09h
    INT 21h
    ; leer número
    MOV DX, OFFSET t82
    MOV AH, 0Ah
    INT 21h
    ; preparar cadena
    MOV SI, OFFSET t82+2
    MOV CL, [t82+1]
    ADD SI, CX
    MOV BYTE PTR [SI], 0
    MOV SI, OFFSET t82+2
    ; texto = t82
    MOV CX, t82    ; Cargar t82
    MOV texto, CX    ; Almacenar en texto
    ; pedir número
    MOV DX, OFFSET str_13
    MOV AH, 09h
    INT 21h
    ; leer número
    MOV DX, OFFSET t83
    MOV AH, 0Ah
    INT 21h
    ; preparar cadena
    MOV SI, OFFSET t83+2
    MOV CL, [t83+1]
    ADD SI, CX
    MOV BYTE PTR [SI], 0
    MOV SI, OFFSET t83+2
    ; caracter = t83
    MOV DX, t83    ; Cargar t83
    MOV caracter, DX    ; Almacenar en caracter
    ; print("El carácter aparece")
    MOV DX, OFFSET str_14
    MOV AH, 09h
    INT 21h
    ; t84 = contar_caracter()
    ; Guardar registros antes de llamar función
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    MOV SI, texto    ; Cargar texto
    MOV texto, SI
    MOV DI, caracter    ; Cargar caracter
    MOV caracter, DI
    CALL contar_caracter
    POP DX
    POP CX
    POP BX
    POP AX
    MOV DI, AX
    MOV t84, DI    ; Almacenar en t84
    MOV AX, t84
    CALL print_number_inline
    ; print("veces.")
    MOV DX, OFFSET str_15
    MOV AH, 09h
    INT 21h
    JMP L53    ; Salto incondicional
L58:
    ; t85 = opcion EQ "5"
    MOV AX, opcion
    ; AL tiene el caracter
    CMP AL, '5'
    JE cmp_true_71
    MOV t85, 0
    JMP cmp_end_71
cmp_true_71:
    MOV t85, 1
cmp_end_71:
    CMP t85, 0
    JE L59    ; Saltar si falso
    ; pedir número
    MOV DX, OFFSET str_8
    MOV AH, 09h
    INT 21h
    ; leer número
    MOV DX, OFFSET t86
    MOV AH, 0Ah
    INT 21h
    ; preparar cadena
    MOV SI, OFFSET t86+2
    MOV CL, [t86+1]
    ADD SI, CX
    MOV BYTE PTR [SI], 0
    MOV SI, OFFSET t86+2
    ; texto = t86
    MOV AX, t86    ; Cargar t86
    MOV texto, AX    ; Almacenar en texto
    ; print("En mayúsculas:")
    MOV DX, OFFSET str_16
    MOV AH, 09h
    INT 21h
    ; t87 = a_mayusculas()
    ; Guardar registros antes de llamar función
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    MOV BX, texto    ; Cargar texto
    MOV texto, BX
    CALL a_mayusculas
    POP DX
    POP CX
    POP BX
    POP AX
    MOV CX, AX
    MOV t87, CX    ; Almacenar en t87
    MOV AX, t87
    CALL print_number_inline
    JMP L53    ; Salto incondicional
L59:
    ; t88 = opcion EQ "6"
    MOV AX, opcion
    ; AL tiene el caracter
    CMP AL, '6'
    JE cmp_true_72
    MOV t88, 0
    JMP cmp_end_72
cmp_true_72:
    MOV t88, 1
cmp_end_72:
    CMP t88, 0
    JE L60    ; Saltar si falso
    ; print(" Saliendo...")
    MOV DX, OFFSET str_17
    MOV AH, 09h
    INT 21h
    JMP L53    ; Salto incondicional
L60:
    ; print(" Opción inválida.")
    MOV DX, OFFSET str_18
    MOV AH, 09h
    INT 21h
L53:
    JMP L50    ; Salto incondicional
L51:
    ; return None
    MOV AX, 0
    RET
menu ENDP

;-------------------------------------------------------
; Programa principal
;-------------------------------------------------------
user_main PROC
    ; t89 = menu()
    ; Guardar registros antes de llamar función
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    CALL menu
    POP DX
    POP CX
    POP BX
    POP AX
    MOV DX, AX
    MOV t89, DX    ; Almacenar en t89
    ; return None
    MOV AX, 0
    RET
user_main ENDP

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
