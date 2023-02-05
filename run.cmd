set NETPORT=80
set IPADDR=127.0.0.1
set DBPATH=c:\projects\emp-data\
set FILES=c:\projects\emp\files\
set IMAGES=c:\projects\emp\images\
set LOGS=c:\projects\emp\logs\
rem
docker run --rm --tty --interactive -p %IPADDR%:%NETPORT%:%NETPORT% -v %DBPATH%:/app/data/ -v %FILES%:/app/files/ -v %IMAGES%:/app/images/ -v %LOGS%:/app/logs/ intranet
rem docker run --rm --tty --interactive -p %IPADDR%:%NETPORT%:%NETPORT% intranet


