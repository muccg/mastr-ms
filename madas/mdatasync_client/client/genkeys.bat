ssh-keygen -q -b 1024 -t rsa -f id_rsa -N ''
move id_rsa "%HOMEDRIVE%%HOMEPATH%\.ssh\id_rsa"
copy id_rsa.pub "%HOMEDRIVE%%HOMEPATH%\.ssh\"
exit
