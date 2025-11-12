.model small
.stack 100h

.data
    str_0  DB '=== CÁLCULO DE FACTORIAL ===', 0Dh, 0Ah, '$'
    str_in DB 0Dh,0Ah,'Ingrese un número: $'
    str_out DB 0Dh,0Ah,'El factorial de ', '$'
    str_es  DB ' es: ', '$'
    newline DB 0Dh,0Ah,'$'

    t4 DB 6, ?, 6 DUP(?)   ; buffer de entrada

    n DW ?
    resultado DW ?
    valor DW ?

.code

main PROC
    mov ax, @data
    mov ds, ax

    call user_main

    mov ah, 4Ch
    int 21h
main ENDP

;-------------------------------------------------------
; factorial: calcula factorial(n) usando pila
; Entrada: AX = n
; Salida: AX = n!
;-------------------------------------------------------
factorial PROC
    cmp ax, 1
    jbe base_case

    push ax        ; guarda n actual
    dec ax         ; n-1
    call factorial ; factorial(n-1)
    pop bx         ; recupera n original
    mul bx         ; AX = factorial(n-1) * n
    ret

base_case:
    mov ax, 1
    ret
factorial ENDP

;-------------------------------------------------------
; Convierte cadena en SI -> AX (entero)
;-------------------------------------------------------
string_to_int PROC
    push bx
    push cx
    push dx
    xor ax, ax
    mov cx, 10
s2i_loop:
    mov bl, [si]
    cmp bl, 0
    je s2i_done
    cmp bl, '0'
    jl s2i_done
    cmp bl, '9'
    jg s2i_done
    sub bl, '0'
    mov bh, 0
    mul cx
    add ax, bx
    inc si
    jmp s2i_loop
s2i_done:
    pop dx
    pop cx
    pop bx
    ret
string_to_int ENDP

;-------------------------------------------------------
; Imprime número (AX)
;-------------------------------------------------------
print_number_inline PROC
    push ax
    push bx
    push cx
    push dx
    push si

    mov cx, 0
    mov bx, 10
    cmp ax, 0
    jge pn_loop
    neg ax
    push ax
    mov dl, '-'
    mov ah, 02h
    int 21h
    pop ax
pn_loop:
    xor dx, dx
    div bx
    push dx
    inc cx
    cmp ax, 0
    jne pn_loop
pn_digits:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop pn_digits

    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
print_number_inline ENDP

;-------------------------------------------------------
; Programa principal
;-------------------------------------------------------
user_main PROC
    ; título
    mov dx, OFFSET str_0
    mov ah, 09h
    int 21h

    ; pedir número
    mov dx, OFFSET str_in
    mov ah, 09h
    int 21h

    ; leer número
    mov dx, OFFSET t4
    mov ah, 0Ah
    int 21h

    ; preparar cadena
    mov si, OFFSET t4+2
    mov cl, [t4+1]
    add si, cx
    mov byte ptr [si], 0
    mov si, OFFSET t4+2

    ; convertir
    call string_to_int
    mov n, ax
    mov valor, ax

    ; calcular factorial
    mov ax, n
    call factorial
    mov resultado, ax

    ; imprimir resultado
    mov dx, OFFSET str_out
    mov ah, 09h
    int 21h

    mov ax, valor
    call print_number_inline

    mov dx, OFFSET str_es
    mov ah, 09h
    int 21h

    mov ax, resultado
    call print_number_inline

    mov dx, OFFSET newline
    mov ah, 09h
    int 21h

    ret
user_main ENDP

END main
