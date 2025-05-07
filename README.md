# rason_integrator
sistem integrasi data rason yang dikirimkan dari aplikasi rason ke server vm collecting
alur pada sistem: 
docker ps -a
- ftp-receiver-rason
- bmkgsatu-sender-rason
- rason-forwarder-ascii
- rason-forwarder-binary

pengiriman file ke folder ftp /ftp/rasonftp/ 
berupa file binery ( bufr, bin ) dan ascii ( .DAT / .X) kemudian dibaca oleh
ftp-receiver-rason  jika sudah diproses maka akan dikirimkan ke RabiitMQ dan
bmkgsatu-sender-rason. file sudah diproses akan dikirim difolder rasonfile-bucket ada ascii dan binary
maka akan diproses oleh - rason-forwarder-ascii  dan  rason-forwarder-binary 

* file binary ( bufr .bin ) yg berhasil dikirimkan ke ftp inaswtiching binary di folder /home/bmkgsatu/rason_integrator/rasonfile-bucket/sent/binary/


cara menjalankan script dengan docker compose
cd rason_integrator/

- docker compose build
- docker compose up
- docker compose down

# cara menjalakan per service
- docker compose stop awos-forwarder
- docker compose start awos-forwarder

# edit script 
- docker compose build ftp-receiver-rason
- docker compose down && docker compose up


# cek logs 
- docker compose logs ftp-receiver-rason
- docker compose logs bmkgsatu-sender
docker compose logs rason-forwarder-
docker compose logs rason-forwarder-ascii
