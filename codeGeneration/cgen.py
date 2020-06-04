def codeGen(tree, file):
    #no compilaba por que para python 3 no reconoce algunas apostrofes por lo que se tuvo que añadir el utf
    f = open(file, "w+",encoding="utf-8")
    recursiveGeneration(tree, f)
    f.close()


def recursiveGeneration(t, f):
    if t:
        current = t[0]
        if current == 'start program':
            f.write('.text\n')
            f.write('.align 2\n')
            f.write('.globl main\n')
            recursiveGeneration(t[1], f)
        elif current in ['statement', 'expression stmt', 'compound stmt', 'return stmt', 'declaration list',
                         'declaration', 'statement list', 'param list', 'param', 'local declarations']:
            for x in range(1, len(t)): recursiveGeneration(t[x], f)
        elif current == 'expression':
            recursiveGeneration(t[3], f) if len(t) == 4 else recursiveGeneration(t[1], f)
        elif current == 'additive expression':
            if len(t) == 4:
                recursiveGeneration(t[1], f)
                f.write('   sw $a0 0($sp)\n')
                f.write('   addiu $sp $sp\n')
                recursiveGeneration(t[3], f)
                if t[2][1] == '+':
                    f.write('   lw $t1 4($sp)\n')
                    f.write('   add $a0 $t1 $a0\n')
                    f.write('   addiu $sp $sp 4\n')
                else:
                    f.write('   lw $t1 4($sp)\n')
                    f.write('   sub $a0 $t1 $a0\n')
                    f.write('   addiu $sp $sp 4\n')
            else: recursiveGeneration(t[1], f)
        elif current == 'term':
            if len(t) == 4:
                recursiveGeneration(t[1], f)
                f.write('   sw $a0 0($sp)\n')
                f.write('   addiu $sp $sp ‐4\n')
                recursiveGeneration(t[3], f)
                if t[2][1] == '*':
                    f.write('   lw $t1 4($sp)\n')
                    f.write('   mult $a0 $t1 $a0\n')
                    f.write('   addiu $sp $sp 4\n')
                else:
                    f.write('   lw $t1 4($sp)\n')
                    f.write('   div $a0 $t1 $a0\n')
                    f.write('   addiu $sp $sp 4\n')
            else:
                recursiveGeneration(t[1], f)
        elif current == 'factor':
            if len(t) == 4: recursiveGeneration(t[2], f)
            else: f.write(f'  li $a0 {t[1]}\n') if type(t[1]) == int else recursiveGeneration(t[1], f)
        elif current == 'selection stmt':
            if len(t) == 6:
                recursiveGeneration(t[3], f)
                f.write('   sw $a0 0($sp)\n')
                f.write('   addiu $sp $sp - 4\n')
                f.write('   lw $t1 4($sp)\n')
                f.write('   addiu $sp $sp 4\n')
                f.write('   beq $a0 $t1 true_branch\n')
                f.write('true_brach:\n')
                recursiveGeneration(t[5], f)
                f.write('b end_if:\n')
            elif len(t) == 8:
                recursiveGeneration(t[3], f)
                f.write('   sw $a0 0($sp)\n')
                f.write('   addiu $sp $sp - 4\n')
                f.write('   lw $t1 4($sp)\n')
                f.write('   addiu $sp $sp 4\n')
                f.write('   beq $a0 $t1 true_branch\n')
                f.write('false_branch:\n')
                recursiveGeneration(t[7], f)
                f.write('   b end_if:\n')
                f.write('true_brach:\n')
                recursiveGeneration(t[5], f)
                f.write('   b end_if:\n')
        elif current == 'simple expression':
            if len(t) == 4:
                recursiveGeneration(t[1], f)
                recursiveGeneration(t[3], f)
                if   t[2][1] == '==': f.write('   beq $a0 $t1 true1\n')
                elif t[2][1] == '>' : f.write('   bgt $a0 $t1 true1\n')
                elif t[2][1] == '<' : f.write('   blt $a0 $t1 true1\n')
                elif t[2][1] == '>=': f.write('   bge $a0 $t1 true1\n')
                elif t[2][1] == '<=': f.write('   ble $a0 $t1 true1\n')
                elif t[2][1] == '!=': f.write('   bne $a0 $t1 true1\n')
            else:
                recursiveGeneration(t[1], f)
        elif current == 'iteration stmt':
            f.write('while:\n')
            for x in range(1, len(t)):
                recursiveGeneration(t[x], f)
            f.write('   j while\n')
            f.write('   exit:\n')
        elif current == 'fun declaration':
            f.write(f'{t[2]}:\n')
            f.write('   move $fp $sp\n')
            f.write('   sw $ra 0($sp)\n')
            f.write('   addiu $sp $sp ‐4\n')
            for x in range(1, len(t)): recursiveGeneration(t[x], f)
            f.write(f'     lw $ra 4($sp)\n')
            f.write(f'     addiu $sp $sp z\n')
            f.write(f'     lw $fp 0($sp)\n')
            f.write(f'     jr $ra\n')
        elif current == 'var declaration':
            if len(t) == 7: f.write(f'  li $a0 {t[2]}\n')
            else: 
                for x in range(1, len(t)): recursiveGeneration(t[x], f)
        elif current == 'params' or current == 'args':
            recursiveGeneration(t[1], f)
        elif current == 'arg list':
            for x in range(1, len(t)): recursiveGeneration(t[x], f)
        elif current == 'var':
            if len(t) == 5: recursiveGeneration(t[3], f)
        elif current == 'call':
            if current == 'input':
                f.write('     li $v0, 5')
                f.write('     syscall')
                f.write('     move $t0, $v0')
            elif current == 'output':
                f.write('     li $v0, 1')
                f.write('     move $a0, $t0')
                f.write('     syscall')
            else:
                f.write('   sw $fp 0($sp)\n')
                f.write('   addiu $sp $sp ‐4\n')
                recursiveGeneration(t[3], f)
                f.write('   sw $a0 0($sp)\n')
                f.write('   addiu $sp $sp ‐4\n')
                f.write(f'  jal {t[1]}\n')
