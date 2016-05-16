import subprocess
import struct
import pwn
import re
import time

def get_timestamp_hash (timestamp) :
    proc = subprocess.Popen('./hive_patched', stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    stdout, stderr = proc.communicate(struct.pack('<L', timestamp))
    return stdout[-33:]



sh = pwn.process('./hive_clean')

initial = sh.recv(1024)
timestr = re.findall('time is: (.*?),', initial)[0]
print '[+] timestr', timestr
timehash = get_timestamp_hash(int(timestr))
print '[+] timehash', timehash
sh.sendline('username')
sh.sendline('5up3rm@n')
sh.sendline(timehash)

time.sleep(1)

# HERE YOU GO AUTHENTICATED

print sh.recv(1024)
print sh.recv(1024)
print sh.recv(1024)



'''
mov rdi, rax
call 0x40a8d0
mov rax, 0x3c
syscall
'''

# at 0x4012e3
'''
lea rcx, [rbp+0xfffffffffffffe64]
push rax
push rbx
push rdx
push rdi
push rsi
push r8
push r9
push r10
push r11
push r12
push r13
push r14
push r15
mov rdx, 4
mov rsi, rcx
mov rdi, 0
mov rax, 0
syscall
pop rax
pop rbx
pop rdx
pop rdi
pop rsi
pop r8
pop r9
pop r10
pop r11
pop r12
pop r13
pop r14
pop r15
mov ecx, [rbp+0xfffffffffffffe64]
jmp 0x40124a
'''


