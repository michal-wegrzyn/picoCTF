from pwn import remote

r = remote('titan.picoctf.net', 65096)

r.recvuntil(b'decrypt.')

with open('password.enc') as file:
    enc_password = int(file.read())

a = 2
r.sendline(b'E')
r.recvuntil(b'keysize): ')
r.sendline(bytes([a]))
r.recvuntil(b'mod n) ')

enc_a = int(r.recvline())

r.sendline(b'D')
r.recvuntil(b'decrypt: ')
r.sendline(str(enc_a*enc_password).encode())
r.recvuntil(b'mod n): ')

password = int(r.recvline(), 16) // a
password = password.to_bytes((password.bit_length() + 7) // 8, 'big').decode('utf-8')

print('Password:', password)
r.close()