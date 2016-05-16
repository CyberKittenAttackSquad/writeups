# hive

Hive, aka nx350, was a 350 point network exploitation challenge, the highest point-value nx challenge, and probably endeavor' favorite. Hive was solved by two people, shareef12 and endeavor.

Hive works in two parts. First, you have to successfully authenticate with the hive server. Second, you have to exploit the service. Endeavor did authentication, shareef12 put together the exploit.

## Authentication - *endeavor*

I seem to have misplaced my [binary ninja](http://binary.ninja/) file with all of my comments, so I'll make this writeup based on what I have. I'm also going to walk through my discovery process, instead of cutting straight to the answer.

The binary comes with symbols stripped, and libc (or some equivalent) statically linked in. Finding out, "Where we are in Kansas," was step number one.

I spent some time shooting around the binary, but eventually ended up just running in GDB, breaking, and tracking my way up the callstack.

```
(gdb) r
Starting program: /vagrant/ctf/jcc2016/nx/hive_clean 
The time is: 1463411643, please hurry with authenticating
Please provide your username: ^C
Program received signal SIGINT, Interrupt.
0x000000000043c550 in ?? ()
(gdb) bt
#0  0x000000000043c550 in ?? ()
#1  0x000000000040cdd0 in ?? ()
#2  0x000000000040f3be in ?? ()
#3  0x000000000040a7d4 in ?? ()
#4  0x000000000040a4e6 in ?? ()
#5  0x00000000004010c0 in ?? ()
#6  0x0000000000401047 in ?? ()
#7  0x0000000000402fe0 in ?? ()
#8  0x0000000000400f07 in ?? ()
(gdb) 
```

Several of these functions didn't disassemble in binary ninja, but I took some of these addresses and started hunting around for function preambles in the binary ninja hex view and manually disassembling functions. Eventually I found my way to sub_401058 (that's #5 in our back trace), and this is the function that handles authentication.

Of course, this wasn't the right way to do find this function. The right way to do this would be to start from `_start`, find `main`, and we would have found this function as the second one called. Normally this is what I would have done, but when there are only a few hours left in the CTF and you're desparate for points *sometimes* the decision making progress is a little flawed.

Let's go to `main` and take a look.

![binary ninja main()](https://github.com/CyberKittenAttackSquad/writeups/raw/master/jcc2016/nx/hive/images/scaled/bn-main.png)

`do_authenticaton` is where our authentication takes place, and `target_function` is where we do our exploitation. I started on `do_authentication`.

About this time shareef12 came on slack and said `!working nx350`, which is our shorthand for announcing what we're working on. We spoke for a few minutes, and agreed shraeef12 would work the exploit and I would work auth.

About 30 minutes later re400, *movfu*, came up, and I switched over to *movfu*, leaving *hive* to shareef12. Shareef12 got a working local exploit in a couple hours, and I came back to finish the authentication.

Diving into the `do_authentication` function.

![binary ninja do_authenicate() 1](https://github.com/CyberKittenAttackSquad/writeups/raw/master/jcc2016/nx/hive/images/scaled/bn-do_authentication_1.png)
![binary ninja do_authenicate() 2](https://github.com/CyberKittenAttackSquad/writeups/raw/master/jcc2016/nx/hive/images/scaled/bn-do_authentication_2.png)

This function reads in three strings, a username, password, and token. The username is never used. I wasn't entirely sure what was going on here, so I broke before and after several of these functions, observing arguments going in and either the results or changes to buffers coming out. I have lost most of these comments, but in short for some of these calls I was observing strings going in, and 16-byte hexadecimal strings coming out.

I believed this was an MD5 function, but couldn't quite figure out what was gong on. Eventually I opened up the function now labeled `md5_string`, and the second function in there, `sub_4024d0` sets the `A`, `B`, `C`, `D` MD5 hash primitives. I now knew this `md5_string` function was correct.

![binary ninja md5_string()](https://github.com/CyberKittenAttackSquad/writeups/raw/master/jcc2016/nx/hive/images/scaled/bn-md5_string.png)
![binary ninja sub_4024d0()](https://github.com/CyberKittenAttackSquad/writeups/raw/master/jcc2016/nx/hive/images/scaled/bn-sub_4024d0.png)

The problem I was having here was not initially accounting for newlines being appended to the ends of my input strings. Once I understood the case, I could create the MD5 hashes needed, and verified we were using md5 here.

Pseudocode, non-valid C for this function, which is not 100% accurate but more-or-less functionally correct, would be:

```c
do_authenticate (long timestamp) {
    print_string("enter username");
    char pass[64] = get_string();
    print_string("enter password");
    char pass[64] = get_string();
    char * tmp = md5_string(pass, strlen(pass));
    strcpy(pass, tmp);
    print_string("enter token");
    char token[64] = get_string();
    strcat(pass, token);
    tmp = md5_string(pass, strlen(pass));
    strcpy(pass, tmp);
    probable_validate(pass, timestamp);
}
```

Moving forward to the function called `probable_validate`.

![binary ninja probable_validate() 1](https://github.com/CyberKittenAttackSquad/writeups/raw/master/jcc2016/nx/hive/images/scaled/bn-probable_validate_1.png)
![binary ninja probable_validate() 2](https://github.com/CyberKittenAttackSquad/writeups/raw/master/jcc2016/nx/hive/images/scaled/bn-probable_validate_2.png)

By setting GDB breakpoints and observing functions, I noticed we first perform some arithmetic over the timestamp, divide the original timestamp by this arithmetic, sprintf the result and `md5_string` it. We then do some permutation over a string pushed onto the stack, and this string looks like an md5 hash. We `strcat` the permutated string and the timestamp md5 hash together, md5 hash those, and compare that to the string we passed into `probable_validate(const char *, long)`.

By setting some breakpoints, we discover what the permutated string is.

```
Starting program: /vagrant/ctf/jcc2016/nx/hive_clean 
The time is: 1463413283, please hurry with authenticating
Please provide your username: user
Please provide your personal password: pass
Please provide an authentication token: token

Breakpoint 1, 0x0000000000401360 in ?? ()
(gdb) x/s $rdi
0x7fffffffe000: "5982aa26412a5dcd5b3d4ec740612d85"
(gdb) x/s $rsi
0x7fffffffdf80: "dbfb89a8706a2f47a30c7b8e49228218"
(gdb) 
```

The permutated string is `"5982aa26412a5dcd5b3d4ec740612d85"`. Pseudocode, non-valid C for this function, which is not 100% accurate but more-or-less functionally correct, would be:

```c
probable_validate (const char * auth_string, long timestamp) {
    long tmp = timestamp;
    do_some_stuff_to_tmp(&tmp);
    tmp = timestamp / tmp;
    char buf[32];
    sprintf(buf, "%d", tmp);
    const char * md5_timestamp = md5_string(buf, strlen(buf));
    char buf[64] = "8215nn59745n8qpq8o6q7rp073945q18";
    permutate_string(buf);
    strcat(buf, md5_timestamp);
    const char * result_hash = md5_string(buf);
    strcpy(buf, result_hash);
    if (strcmp(auth_string, buf)) {
        FAIL();
    }
    else {
        PASS();
    }
}
```

Based off this information, we need our two strings in `do_authentication`, IE the *password* and *token* strings, to be equal to the two strings passed to `strcat` in `probable_validate`. A quick google of the first hash, `5982aa26412a5dcd5b3d4ec740612d85`, returns the string `"5up3rm@n"`. This is our password.

The second string in `probable_validate` is based off a timestamp. Not wanting to bother with reversing the arithmetic taking place, I decided to patch the `hive` binary like so:

1. Nop out the three calls to `get_string` in `do_authentication`.
2. Replace the instruction at `0x40121d` with a jump to some custom assembly which performs a system call to `read`, and reads in a timestamp.
3. Let the original binary perform the arithmetic and hasing over our given timestamp.
4. Drop in some custom assembly at `0x4012bc` and call `puts` over the md5 hash string of our timestamp.
5. Call exit.

This patched binary is available in the `hive_patched` file. The assembly patches are available as comments in `hiveauth.py`.

I could now code out some interaction code in pwnlib, call my patched binary to get the correct timestamp string, and log into the challenge. The below code to authenticate with the server is available in `hiveauth.py`.

```python
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
```

This was passed on to shareef12, along with the hive_patched binary, so he could integrate this with his exploit and successfully exploit the remote process.


## Exploitation - *shareef12*

The full exploit is available in `nx350.py`. Perhaps shareef12 will come back at a later time and write up the vulnerability.
