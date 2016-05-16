### Shrek

Shrek was a 250 or 300 point reverse-engineering challenge.

I actually have no idea what was in Shrek, or how it was put together.

```python
import subprocess
import os

PINTOOLS_PATH = '/home/dev/source/pin-3.0-76991-gcc-linux/'
TOOL_PATH = os.path.join(PINTOOLS_PATH, 'source/tools/ManualExamples/obj-ia32/inscount0.so')
MOVFU_PATH = '/home/dev/ctf/jcc2016/re/shrek'

chars = '_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789~!@#$%^&*()_+-={}[],./<>?'

def run (s) :
    cmd = [os.path.join(PINTOOLS_PATH, 'pin')]
    cmd += ['-t']
    cmd += [TOOL_PATH]
    cmd += ['--']
    cmd += [MOVFU_PATH]
    cmd += ['"' + s + '"']

    cmd = ' '.join(cmd)

    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    proc.communicate(s)

    fh = open('inscount.out', 'rb')
    raw = fh.read()
    fh.close()
    count, n = raw.strip().split(' ')
    return int(n)


for c in chars :
    print c, run('flag{_On10ns_aRe_a_ta57y_tR3a7_}' + c)
```