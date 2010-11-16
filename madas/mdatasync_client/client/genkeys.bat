echo "CWRSYNC HOME IS: %CWRSYNCHOME%"
echo "PATH is : %PATH%"
ssh-keygen.exe -q -b 1024 -t rsa -f id_rsa -N ''
mkdir "%CWRSYNCHOME%\home\%USERNAME%\.ssh\"
move id_rsa "%CWRSYNCHOME%\home\%USERNAME%\.ssh\id_rsa"
copy id_rsa.pub "%CWRSYNCHOME%\home\%USERNAME%\.ssh\"
exit
