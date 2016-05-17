# labyrinth

Labyrinth was a 300 point re challenge. This challenge is broken down into four stages. The binary starts up a bind tcp fork server on port 9999. Connecting to the server, we're presented with the following prompt:

```
Welcome to the Labyrinth.  If you can navigate the deadly maze and answer the Guardian's riddles you will find the knowledge you seek...
Which direction will you go?
(Enter the numeric value)
1 : Forward
2 : Left
3 : Right
```

Diving into the binary, we find these conditional jumps based on return values from the `check_input` function:

![bn-one](https://github.com/CyberKittenAttackSquad/writeups/raw/master/jcc2016/re/labyrinth/images/scaled/bn-one.png)

The `check_input` function ensures our input is either `0x31`, `0x32`, or `0x33`, subtracts `0x30` from the input, and returns. This turns ASCII `'1'` to the byte value `0x1`, and so on. We find the first values needed to continue are: `12113`.

Moving on, we are presented with a question:

```
Welcome to the Labyrinth.  If you can navigate the deadly maze and answer the Guardian's riddles you will find the knowledge you seek...
Which direction will you go?
(Enter the numeric value)
1 : Forward
2 : Left
3 : Right
1
2
1
1
3
You come face to face with a large creature with a squid-like face.
A voice booms within your head!
When referring to computer memory, what does that acronym RAM stand for?
```

Taking a look at the code for these questions, we see we're pulling a pointer to the question from memory.

![bn-two](https://github.com/CyberKittenAttackSquad/writeups/raw/master/jcc2016/re/labyrinth/images/scaled/bn-two.png)

Following the pointers....

![bn-three](https://github.com/CyberKittenAttackSquad/writeups/raw/master/jcc2016/re/labyrinth/images/scaled/bn-three.png)

![bn-four](https://github.com/CyberKittenAttackSquad/writeups/raw/master/jcc2016/re/labyrinth/images/scaled/bn-four.png)

We arrive at the questions and the answers in strings. We code those up in a lookup table so we can solve them:

```
questions_1 = []
questions_1.append(['When referring to computer', 'Random Access Memory'])
questions_1.append(['With over 17 million units', 'Commodore 64'])
questions_1.append(['Who is credited with', 'Charles Babbage'])
questions_1.append(['How many Gigabytes are', '1024'])
questions_1.append(['Crash Override and Acid Burn', 'Hackers'])
questions_1.append(['___ the Planet', 'Hack'])
questions_1.append(['What linux distro', 'Slackware'])
questions_1.append(['Also known as', 'Johnny Long'])
```

The next two stages are identical to the first stage, with the exception that the directions change. The same questions are used.

The fourth stage looks like this:

```
You've done well to make it this far.  To find the knowledge you seek you must answer my final question:
V2hhdCBlbmNvZGluZyBzY2hlbWUgaXMgdGhpcyBxdWVzdGlvbiB1c2luZz8=
```

Decoding the base64, we get the question, "What encoding scheme is this question using?."

If we look at the assembly, we'll see our answer to this question will go through a function called `translatify`, and then a `strncmp` will take place between the result of our translatified string and `"base64"`

![bn-five](https://github.com/CyberKittenAttackSquad/writeups/raw/master/jcc2016/re/labyrinth/images/scaled/bn-five.png)

Let's take a look at `translatify`.

![bn-translatify](https://github.com/CyberKittenAttackSquad/writeups/raw/master/jcc2016/re/labyrinth/images/scaled/bn-translatify.png)

This just has nope written all over it. We need an input for translatify that will cause the first 6 characters of the output to be base64. Is there another way to solve this without reversing this function?

Why yes, yes there is.

We will nop out all of the socket/fork stuff, nop out stages 1, 2, and 3, nop out some more things, and turn this binary into a simple program that reads in a string, and outputs the result of translatify. We then write up some simple genetic-algorithm-ishy code around this binary, and continually mutate our input until we find one that results in BASE64. Upon observation, we notice that subsequent characters influence the characters preceeding them, and by solving for BASE64 in order, or algorithm improves.

The code to solve for the key is in `gen.py`, and you will need to run it with `lab-solve`, which is our patched binary.

The output will look something like:

```
done with family 0
0 aaaaaaaaaaaaaaaaaaa
0 aaaaaaaaaaaaaaaaaaa
0 aaaaaaaaaaaaaaaaaaa
0 aaaaaaaaaaaaaaaaaaa
0 aaaaaaaaaaaaaaaaaaa
...
done with family 20
3 QmFzwl"{AtHSX*MpTa+
3 QmFzw?"{AbH_X*MpTaU
3 QmFzDP"8m=H@X6DMqaU
3 QmFz@lE{A,H@X%Qpwac
3 QmFzwl"{A1H@XrMpT8P
...
done with family 84
5 YmFzZTaxS!G*G|jCDE%
5 YmFzZTaNMuQjltjg@ES
5 QmFzZTaxIOC)#ezAya7
5 QmFzZTaH8$n8U_U"3]3
```

The numbers on the left represent how many characters we've solved for. Once it hits 6, we have a string which will result in "BASE64" as the output of translatify. We are almost done.

Once we've passed translatify, the remote server will password protect the binary with `keyData`.

![bn-keydata](https://github.com/CyberKittenAttackSquad/writeups/raw/master/jcc2016/re/labyrinth/images/scaled/bn-keydata.png)

Running the binary a couple of times we notice that `keyData` will be equal to `BBBBAAAACCCCBASE64` where `BBBB` is the first four characters of the answer to our second question, `AAAA` is the first four character of the answer to our first question, and `CCCC` is the first four characters of the answer to our third question. Keep in our inputs will be uppercased by the binary.

We now have everything we need to solve the challenge, retrieve the remote binary, and decrypt it.

Code to solve this challenge is in `labyrinth.py`