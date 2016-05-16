This is a web application which lets us log in using a username,
password, and email. Once we login, we are provided with a cookie. We know that AES is being used, but we do not know the encryption mode used.

One of the main issues when examining cookies is determining if there is any pattern between user input and resulting cookie. Discerning this input-out relationship is closely related to detecting the cipher mode used.  

One method of detecting if an encrypted cookie is using a weak mode (like ECB) is by solving the longest common substring problem. Usually ECB mode detection is demonstrated visually (https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Electronic_Codebook_.28ECB.29), but by computing the least common substring of cookies you can detect cipher modes that preserve plaintext patterns. 

Let's say you have cookies `e04a8615810d47c9feb9ac06df600ff0799a5dc4824d8f51e2a78524b1020705a6eaf0fe5db99c6755c21f277aff95020ea7708a8f28694887deb53b8ecd855ba90ef9d9ab0a1d5913baf5f4c592e484` and `32affc73397fb19aa02584ae58303cdb799a5dc4824d8f51e2a78524b1020705a6eaf0fe5db99c6755c21f277aff95020ea7708a8f28694887deb53b8ecd855b52e5c58271840c72e4ef70f717dd31e4` 

Computing the longest common substring will give you longest string that is a substring of two or more strings. This will show if there any plaintext data patterns in the ciphertext. 

In this case the longest common substring is `799a5dc4824d8f51e2a78524b1020705a6eaf0fe5db99c6755c21f277aff95020ea7708a8f28694887deb53b8ecd855b`.  

A long common substring tells you that the two encrypted cookies share data and usually means that ECB mode was used. The first cookies was created using the username 'a' and email 'a'. The second cookie was created using email 'b' and username 'b'. 

Once we know ECB mode is being used, then we can mount a cut-paste-and-attack.  
