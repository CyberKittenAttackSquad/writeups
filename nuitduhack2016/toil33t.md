This is a web application which lets us log in using a username,
password, and email. Once we login, we are provided with a cookie.

On of the main issues when examining cookies is determining if there
is any pattern. One method of detecting if an encrypted cookie is
using ECB mode is by solving the longest common substring
problem. Usually ECB mode is detection is demonstrated visually
(https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Electronic_Codebook_.28ECB.29),
but by computing the least common substring of cookies you can detect
ECB mode. 
