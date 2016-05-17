import pwn
import time

SLEEP_DELAY = 0.2

questions_1 = []
questions_1.append(['When referring to computer', 'Random Access Memory'])
questions_1.append(['With over 17 million units', 'Commodore 64'])
questions_1.append(['Who is credited with', 'Charles Babbage'])
questions_1.append(['How many Gigabytes are', '1024'])
questions_1.append(['Crash Override and Acid Burn', 'Hackers'])
questions_1.append(['___ the Planet', 'Hack'])
questions_1.append(['What linux distro', 'Slackware'])
questions_1.append(['Also known as', 'Johnny Long'])

sh = pwn.remote('10.211.55.5', 9999)
#104.196.32.94:9999
#sh = pwn.remote('104.196.32.94', 9999)

print 'BEGIN SECTION ONE'
print 'moving'
time.sleep(SLEEP_DELAY)
sh.send('1')
time.sleep(SLEEP_DELAY)
sh.send('2')
time.sleep(SLEEP_DELAY)
sh.send('1')
time.sleep(SLEEP_DELAY)
sh.send('1')
time.sleep(SLEEP_DELAY)
sh.send('3')
time.sleep(SLEEP_DELAY)
print 'done moving'
while True :
    question_found = False
    question = sh.recv(1024)
    for q in questions_1 :
        if q[0] in question :
            sh.send(q[1].upper())
            print '\t', q[1].upper()
            question_found = True
    if question_found :
        break
print 'done with monster'
print 'END SECTION ONE'

time.sleep(SLEEP_DELAY)

print 'BEGIN SECTION TWO'
print 'moving'
sh.send('3')
time.sleep(SLEEP_DELAY)
sh.send('1')
time.sleep(SLEEP_DELAY)
sh.send('1')
time.sleep(SLEEP_DELAY)
sh.send('2')
time.sleep(SLEEP_DELAY)
sh.send('1')
time.sleep(SLEEP_DELAY)
print 'done moving'
while True :
    question_found = False
    question = sh.recv(1024)
    for q in questions_1 :
        if q[0] in question :
            sh.send(q[1].upper())
            print '\t', q[1].upper()
            question_found = True
    if question_found :
        break
print 'done with question'
print 'END SECTION TWO'

print 'BEGIN SECTION THREE'
print 'moving'
sh.send('3')
time.sleep(SLEEP_DELAY)
sh.send('1')
time.sleep(SLEEP_DELAY)
sh.send('1')
time.sleep(SLEEP_DELAY)
sh.send('2')
time.sleep(SLEEP_DELAY)
sh.send('1')
time.sleep(SLEEP_DELAY)
print 'done moving'
while True :
    question_found = False
    question = sh.recv(1024)
    print question
    for q in questions_1 :
        if q[0] in question :
            sh.send(q[1].upper())
            print '\t', q[1].upper()
            question_found = True
    if question_found :
        break
print 'done with question'
print 'END SECTION THREE'

time.sleep(SLEEP_DELAY)
print sh.recv(1024)
print 'SENDING FINAL CHALLENGE'
sh.send('QmFzZTY0gTX=)Bb(=G^')
print 'END FINAL CHALLENGE'

print sh.recv(1024)

prize = sh.recvall()

fh = open('/tmp/prize', 'wb')
fh.write(prize)
fh.close()