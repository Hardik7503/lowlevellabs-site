# ARM (32-bit) Exercises: Corrected Solutions

Legend: 🔧 = bug fixed, ✅ = already correct (only tidied/commented).  
Note: Linux process exit codes are 8-bit; a result of -7 appears as 249 in `echo $?`.

## Prog 23: Sum 1 to 5 ✅
Expected: 15

```asm
.section .text
.global _start
_start:
    mov r0, #0
    mov r1, #1
    mov r2, #5
loop:
    add r0, r0, r1
    add r1, r1, #1
    cmp r1, r2
    ble loop
exit:
    mov r7, #1
    svc #0
```

## Prog 27: Max element ✅
Expected: 23

```asm
.section .data
nums: .word 4, 17, 9, 23, 5
len:  .word 5
.section .text
.global _start
_start:
    ldr r3, =nums
    ldr r2, =len
    ldr r2, [r2]
    ldr r0, [r3]
    mov r1, #1
loop:
    cmp r1, r2
    bge exit
    ldr r4, [r3, r1, LSL #2]
    cmp r4, r0
    movgt r0, r4
    add r1, r1, #1
    b loop
exit:
    mov r7, #1
    svc #0
```

## Prog 28: Sum of all elements ✅
Expected: 30

```asm
.section .data
nums: .word 2, 4, 6, 8, 10
len:  .word 5
.section .text
.global _start
_start:
    mov r0, #0
    mov r1, #0
    ldr r2, =len
    ldr r2, [r2]
    ldr r3, =nums
arr_loop:
    cmp r1, r2
    bge exit
    ldr r4, [r3, r1, LSL #2]
    add r0, r0, r4
    add r1, r1, #1
    b arr_loop
exit:
    mov r7, #1
    svc #0
```

## Prog 31: Sum elements divisible by 3 ✅
Expected: 24. Requires an ARM CPU supporting `sdiv`.

```asm
.section .data
nums: .word 3, 5, 9, 10, 12, 14
len: .word 6
.section .text
.global _start
_start:
    mov r0, #0
    mov r1, #0
    ldr r2, =len
    ldr r2, [r2]
    mov r5, #3
    ldr r3, =nums
arr_loop:
    cmp r1, r2
    bge exit
    ldr r4, [r3, r1, LSL #2]
    sdiv r6, r4, r5
    mul r6, r6, r5
    subs r6, r4, r6
    bne next_loop
    add r0, r0, r4
next_loop:
    add r1, r1, #1
    b arr_loop
exit:
    mov r7, #1
    svc #0
```

## Prog 32: Minimum element ✅
Expected: -8 (exit status 248)

```asm
.section .data
nums: .word 7, -3, 12, -8, 5
len: .word 5
.section .text
.global _start
_start:
    ldr r2, =len
    ldr r2, [r2]
    ldr r3, =nums
    ldr r0, [r3]
    mov r1, #1
arr_loop:
    cmp r1, r2
    bge exit
    ldr r4, [r3, r1, LSL #2]
    cmp r4, r0
    movlt r0, r4
    add r1, r1, #1
    b arr_loop
exit:
    mov r7, #1
    svc #0
```

## Prog 35: Maximum absolute value 🔧
Expected: 22. The loop comparison must be `cmp r1, r2`, not `cmp r2, r1`.

```asm
.section .data
nums: .word 4, -15, 9, -22, 7
len: .word 5
.section .text
.global _start
_start:
    mov r1, #0
    ldr r2, =len
    ldr r2, [r2]
    ldr r3, =nums
    ldr r4, [r3, r1, LSL #2]
    cmp r4, #0
    rsblt r0, r4, #0
    movge r0, r4
    add r1, r1, #1
arr_loop:
    cmp r1, r2
    bge exit
    ldr r4, [r3, r1, LSL #2]
    cmp r4, #0
    rsblt r5, r4, #0
    movge r5, r4
    cmp r5, r0
    movgt r0, r5
    add r1, r1, #1
    b arr_loop
exit:
    mov r7, #1
    svc #0
```

## Prog 36: Index of maximum value ✅
Expected: 3

```asm
.section .data
nums: .word 6, 18, 3, 25, 10
len: .word 5
.section .text
.global _start
_start:
    ldr r2, =len
    ldr r2, [r2]
    ldr r3, =nums
    ldr r0, [r3]
    mov r5, #0
    mov r1, #1
arr_loop:
    cmp r1, r2
    bge exit
    ldr r4, [r3, r1, LSL #2]
    cmp r4, r0
    ble next_loop
    mov r0, r4
    mov r5, r1
next_loop:
    add r1, r1, #1
    b arr_loop
exit:
    mov r0, r5
    mov r7, #1
    svc #0
```

## Prog 39: Count values divisible by 4 ✅
Expected: 4

```asm
.section .data
nums: .word 4, 7, 12, 16, 5, 20
len: .word 6
.section .text
.global _start
_start:
    mov r0, #0
    mov r1, #0
    ldr r2, =len
    ldr r2, [r2]
    ldr r3, =nums
arr_loop:
    cmp r1, r2
    bge exit
    ldr r4, [r3, r1, LSL #2]
    ands r5, r4, #3
    bne next_loop
    add r0, r0, #1
next_loop:
    add r1, r1, #1
    b arr_loop
exit:
    mov r7, #1
    svc #0
```

## Prog 40: Index of first even element ✅
Expected: 3

```asm
.section .data
nums: .word 7, 9, 5, 12, 3, 8
len: .word 6
.section .text
.global _start
_start:
    mov r0, #-1
    mov r1, #0
    ldr r2, =len
    ldr r2, [r2]
    ldr r3, =nums
arr_loop:
    cmp r1, r2
    bge exit
    ldr r4, [r3, r1, LSL #2]
    ands r5, r4, #1
    bne next_loop
    mov r0, r1
    b exit
next_loop:
    add r1, r1, #1
    b arr_loop
exit:
    mov r7, #1
    svc #0
```

## Prog 43: Last index of element greater than 10 ✅
Expected: 5

```asm
.section .data
nums: .word 4, 7, 3, 15, 8, 20
len: .word 6
.section .text
.global _start
_start:
    mov r0, #-1
    mov r1, #0
    ldr r2, =len
    ldr r2, [r2]
    ldr r3, =nums
arr_loop:
    cmp r1, r2
    bge exit
    ldr r4, [r3, r1, LSL #2]
    cmp r4, #10
    ble next_loop
    mov r0, r1
next_loop:
    add r1, r1, #1
    b arr_loop
exit:
    mov r7, #1
    svc #0
```

## Prog 44: Count negative numbers ✅
Expected: 3

```asm
.section .data
nums: .word 5, -3, 12, -7, 9, -1
len: .word 6
.section .text
.global _start
_start:
    mov r0, #0
    mov r1, #0
    ldr r2, =len
    ldr r2, [r2]
    ldr r3, =nums
arr_loop:
    cmp r1, r2
    bge exit
    ldr r4, [r3, r1, LSL #2]
    cmp r4, #0
    bge next_loop
    add r0, r0, #1
next_loop:
    add r1, r1, #1
    b arr_loop
exit:
    mov r7, #1
    svc #0
```

## Prog 47: Smallest negative number ✅
Expected: -7 (exit status 249)

```asm
.section .data
nums: .word 5, -3, 12, -7, 9, -1
len: .word 6
.section .text
.global _start
_start:
    mov r0, #0
    mov r1, #0
    ldr r2, =len
    ldr r2, [r2]
    ldr r3, =nums
arr_loop:
    cmp r1, r2
    bge exit
    ldr r4, [r3, r1, LSL #2]
    cmp r4, #0
    bge next_loop
    cmp r4, r0
    bge next_loop
    mov r0, r4
next_loop:
    add r1, r1, #1
    b arr_loop
exit:
    mov r7, #1
    svc #0
```

## Prog 48: Index of smallest negative number ✅
Expected: 3

```asm
.section .data
nums: .word 5, -3, 12, -7, 9, -1
len: .word 6
.section .text
.global _start
_start:
    mov r0, #-1
    mov r5, #0
    mov r1, #0
    ldr r2, =len
    ldr r2, [r2]
    ldr r3, =nums
arr_loop:
    cmp r1, r2
    bge exit
    ldr r4, [r3, r1, LSL #2]
    cmp r4, #0
    bge next_loop
    cmp r0, #-1
    beq update
    cmp r4, r5
    bge next_loop
update:
    mov r5, r4
    mov r0, r1
next_loop:
    add r1, r1, #1
    b arr_loop
exit:
    mov r7, #1
    svc #0
```

## Prog 61: Sum of even numbers ✅
Expected: 24

```asm
.section .data
nums: .word 5, -3, 12, -7, 9, -1, 8, 4
len: .word 8
.section .text
.global _start
_start:
    mov r0, #0
    mov r1, #0
    ldr r2, =len
    ldr r2, [r2]
    ldr r3, =nums
arr_loop:
    cmp r1, r2
    bge exit
    ldr r4, [r3, r1, LSL #2]
    tst r4, #1
    bne next_loop
    add r0, r0, r4
next_loop:
    add r1, r1, #1
    b arr_loop
exit:
    mov r7, #1
    svc #0
```

## Prog 62: Count multiples of 8 ✅
Expected: 4

```asm
.section .data
nums: .word 5, 8, 12, 16, 24, 7, 32
len: .word 7
.section .text
.global _start
_start:
    mov r0, #0
    mov r1, #0
    ldr r2, =len
    ldr r2, [r2]
    ldr r3, =nums
arr_loop:
    cmp r1, r2
    bge exit
    ldr r4, [r3, r1, LSL #2]
    ands r5, r4, #7
    bne next_loop
    add r0, r0, #1
next_loop:
    add r1, r1, #1
    b arr_loop
exit:
    mov r7, #1
    svc #0
```

## Prog 65: Structure, set READY bit 🔧
Expected: 1. Fixed `.global _start` spacing and `pop {lr}`.

```asm
.section .data
device:
    .word 100
    .word 55
    .word 0
.section .text
.global _start
_start:
    ldr r0, =device
    bl set_ready
    ldr r1, [r0, #8]
    mov r0, r1
    mov r7, #1
    svc #0
set_ready:
    push {lr}
    ldr r1, [r0, #8]
    orr r1, r1, #1
    str r1, [r0, #8]
    pop {lr}
    bx lr
```

## Prog 69: Function sum_array 🔧
Expected: 100. Fixed array addressing to use loop index `r4`.

```asm
.section .data
nums: .word 10, 20, 30, 40
len: .word 4
.section .text
.global _start
_start:
    ldr r0, =nums
    ldr r1, =len
    ldr r1, [r1]
    bl sum_array
    mov r7, #1
    svc #0
sum_array:
    push {r4-r6, lr}
    mov r4, #0
    mov r5, #0
arr_loop:
    cmp r4, r1
    bge done
    ldr r6, [r0, r4, LSL #2]
    add r5, r5, r6
    add r4, r4, #1
    b arr_loop
done:
    mov r0, r5
    pop {r4-r6, lr}
    bx lr
```

## Prog 70: Function max_array 🔧
Expected: 99. Fixed invalid `mov r5, [r0]` to `ldr r5, [r0]` and corrected the max update direction.

```asm
.section .data
nums: .word 10, 55, 23, 99, 41
len: .word 5
.section .text
.global _start
_start:
    ldr r0, =nums
    ldr r1, =len
    ldr r1, [r1]
    bl max_array
    mov r7, #1
    svc #0
max_array:
    push {r4-r6, lr}
    ldr r5, [r0]
    mov r4, #1
arr_loop:
    cmp r4, r1
    bge done
    ldr r6, [r0, r4, LSL #2]
    cmp r6, r5
    ble next_loop
    mov r5, r6
next_loop:
    add r4, r4, #1
    b arr_loop
done:
    mov r0, r5
    pop {r4-r6, lr}
    bx lr
```

## Prog 73: Function min_max ✅
Expected: min = 3 (r0), max = 88 (r1). The exit code displays the low 8 bits of r0.

```asm
.section .data
nums: .word 42, 7, 19, 3, 88, 25
len: .word 6
.section .text
.global _start
_start:
    ldr r0, =nums
    ldr r1, =len
    ldr r1, [r1]
    bl min_max
    mov r7, #1
    svc #0
min_max:
    push {r4-r7, lr}
    ldr r6, [r0]
    mov r7, r6
    mov r4, #1
arr_loop:
    cmp r4, r1
    bge done
    ldr r5, [r0, r4, LSL #2]
    cmp r5, r6
    movlt r6, r5
    cmp r5, r7
    movgt r7, r5
    add r4, r4, #1
    b arr_loop
done:
    mov r0, r6
    mov r1, r7
    pop {r4-r7, lr}
    bx lr
```
