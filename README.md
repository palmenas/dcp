# Decrypt Chrome Browser Passwords
I created this tool to decrypt chrome based browser saved passwords in `Login Data` database file.

This tool was addapted from https://github.com/ohyicong/decrypt-chrome-passwords. If you want a better
understanding on how this tool works, please see the following posts:

- https://palmenas.medium.com/forensic-recovery-of-chrome-based-browser-passwords-e8df90d4a3cd
- https://ohyicong.medium.com/how-to-hack-chrome-password-with-python-1bedc167be3d

In order to fully decrypt the passwords, you need the following data:
* User's DPAPI masterkey
* `Login Data` database file
* `Local State` json user file
* Python3, mimikatz, memprocfs

# OS Support
This tool was tested in Linux and Windows

# References
Full credits on the original tool to https://github.com/ohyicong/decrypt-chrome-passwords
