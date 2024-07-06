# rsa_oracle

Link to the challenge: https://play.picoctf.org/practice/challenge/422

## Description

Can you abuse the oracle?
An attacker was able to intercept communications between a bank and a fintech company. They managed to get the message (ciphertext) and the password that was used to encrypt the message.
After some intensive reconassainance they found out that the bank has an oracle that was used to encrypt the password and can be found here `nc titan.picoctf.net 65096`. Decrypt the password and use it to decrypt the message. The oracle can decrypt anything except the password.

### Note that you may receive different port numbers.

# Solution

## Sample interaction

We can communicate with the oracle to encrypt and decrypt data as shown below:

```
$ nc titan.picoctf.net 65096
*****************************************
****************THE ORACLE***************
*****************************************
what should we do for you? 
E --> encrypt D --> decrypt. 
E
enter text to encrypt (encoded length must be less than keysize): text
text

encoded cleartext as Hex m: 74657874

ciphertext (m ^ e mod n) 667159474168492952744964328002523639589850331698353348971365625582640848075733466290181680755671514559653277095818871225924389160702832850093794553930825

what should we do for you? 
E --> encrypt D --> decrypt. 
D
Enter text to decrypt: 667159474168492952744964328002523639589850331698353348971365625582640848075733466290181680755671514559653277095818871225924389160702832850093794553930825
decrypted ciphertext as hex (c ^ d mod n): 74657874
decrypted ciphertext: text

what should we do for you? 
E --> encrypt D --> decrypt. 
^C
```

## RSA homomorphic property
RSA encryption is multiplicatively homomorphic, meaning:

$E(m_1​)\times E(m_2​)=(m_1^e~mod~n)\times(m_2^e~​mod~n)=(m_1​\times m_2​)^e~mod~n=E(m1​\times m2​)$

This property allows us to manipulate ciphertexts in a way that the result, when decrypted, gives us the product of the original plaintexts.

## Attack steps

### 1. Encrypt a Known Value $a$:
- Choose a small known value $a$, for instance, 2.
- Request the oracle to encrypt $a$. Let the encrypted value be $E(a)$.
  
### 2. Multiply the Ciphertexts:
- Suppose the encrypted password in `password.enc` is $E(p)$, where $p$ is the password.
- Compute $E(a)\times E(p) = E(a \times p)$
- Send $E(a\times p)$ to the oracle for decryption. The oracle will decrypt and return $a\times p$.

### 3. Retrieve the Original Password:
- Since $a$ is known, divide the result by $a$ to retrieve $p$:
$$p=\frac{a\times p}{a}$$

### These steps are implemented in `script.py` file.

## Capture the flag

### 1. Run the script to get the password:
```
$ python3 script.py
[+] Opening connection to titan.picoctf.net on port 65096: Done
Password: da099
[*] Closed connection to titan.picoctf.net port 65096
```

### 2. Decrypt `secret.enc` using OpenSSL
```
$ openssl enc -aes-256-cbc -d -in secret.enc
enter AES-256-CBC decryption password:
*** WARNING : deprecated key derivation used.
Using -iter or -pbkdf2 would be better.
picoCTF{su((3ss_(r@ck1ng_r3@_da099d93}
```

### Flag: picoCTF{su((3ss_(r@ck1ng_r3@_da099d93}