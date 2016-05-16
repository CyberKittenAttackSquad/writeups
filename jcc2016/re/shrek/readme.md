# shrek

Shrek was a 250 or 300 point reverse-engineering challenge, I can't remember

I actually have no idea what was in Shrek, or how it was put together. I had some code available for blackbox analyzing challenges like this, and I adpated it for Shrek.

You will need [pintools](https://software.intel.com/en-us/articles/pin-a-dynamic-binary-instrumentation-tool) installed for this challenge to work, and you will need to build the ManualExamples found in source/tools/ManualExamples. Adjust the paths.

Down at the end where you see `run('flag{_On10ns_aRe_a_ta57y_tR3a7_}' + c)` replace with `run('' + c)`. You'll get the output of each character, and the number of instructions that were executed with that character fed as input.

For example:

```
_ 97162
a 97162
b 97162
c 97162
d 97162
e 97162
f 97172
g 97162
h 97162
i 97162
j 97162
```

We see that ``f`` took more instructions to execute. Our first character is ``f``. We prepend that to our string passed to ``run()`` and solve for the next character.

This process could be automated, but all in all it took about 10-15 minutes to solve the problem manually. It would have taken more time to fix up the code to solve the problem automatically, make sure it worked right, and run the code.

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