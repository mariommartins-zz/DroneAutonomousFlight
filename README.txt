Autoria: Mario Augusto Mota Martins - 2017 - UFBA
Professor Orientador: Flavio Assis

>>>>>>>Connecting GPS to rapsberry pi 3<<<<<<<
	---Jessie OS---
	
	>A ligação do GPS é vcc (pin 4), gnd (pin 6), rx (pin 8) e tx (pino 10)
	
	>Habilitando miniuart para a porta serial:
		sudo raspi-config
			interfacing
				serial
					yes
	
		sudo nano /boot/cmdline.txt
			enable_uart=1
	
	>Verificando portas seriais
		ls -l /dev
	
	sudo nano /boot/cmdline.txt
	
	(eg, remove console=ttyAMA0,115200 and if there, kgdboc=ttyAMA0,115200 )
	Note you might see console=serial0,115200 or console=ttyS0,115200 and should remove those parts of the line if present
	
	sudo systemctl stop serial-getty@ttyS0.service
	sudo systemctl disable serial-getty@ttyS0.service
	
	sudo systemctl enable gpsd.socket
	sudo systemctl start gpsd.socket 
	
	sudo reboot
	
	sudo killall gpsd
	
	sudo gpsd /dev/ttyS0 -F -n /var/run/gpsd.sock
	(it`s important to use the -n command, so it`ll not return error without waitting for connection properlly)
	
	'
	(It will take a lot of time if you are indoor to find a sattelite, with me it took around an hour next to the window)
	
	sudo cgps -s
		or
	sudo gpsmon /dev/ttyS0
	
	>Referencias
	PRINCIPAL:
	https://cdn-learn.adafruit.com/downloads/pdf/adafruit-ultimate-gps-on-the-raspberry-pi.pdf
	
	https://raspberrypi.stackexchange.com/questions/45570/how-do-i-make-serial-work-on-the-raspberry-pi3/45571#45571?newreg=963a1d6e381c4a19b90ed26745a405a7
	
	https://www.raspberrypi.org/forums/viewtopic.php?f=44&t=51788
	
	http://www.stuffaboutcode.com/2013/09/raspberry-pi-gps-setup-and-python.html

>>>>>>>Acessando raspberry por SSH<<<<<<<

>Ethernet
>>ip=169.254.91.222
>Wifi
>>ip=192.168.1.(entre 2 e 6)

login=pi
password=raspberry

https://anwaarullah.wordpress.com/2013/07/16/direct-access-raspberry-pi-shell-and-desktop/

caso for windows e ele n reconheça a conexão, resete o adapter
	win+r
		devmgmt.msc
			Network adapters
				Realtek PCIe GBE Family Controller
					Disable + Enable

>>>>>>>Rodando o Codigo<<<<<<<
	Abre Terminal
	python <nomeDoArquivo>

>>>>>>>Teste de calculo de angulação<<<<<<<

	Rota:
		UFBA
			Lat:-13.002486
			Lng:-38.509006
		Casa
			Lat:-12.893512
			Lng:-38.459275


>>>>>>>Desativar módulos para economia de bateria<<<<<<<
>Módulo HDMI
>>Desativar
/opt/vc/bin/tvservice -o 
>>Ativar
/opt/vc/bin/tvservice -p

>>>>>>>Conectar e desconectar do AP ar.drone<<<<<<<<<<<<<
>Para conectar e desconectar deve-se adicionar a network em um arquivo chamado wpa_supplicant.conf
> e atualizar um arquivo chamado interfaces para conectar automaticamente em redes wifi preconfiguradas

cd /etc/network
sudo nano interfaces

>modifica todo o conteudo da linha que contém "wlan0", colocando antes de "wlan0" apenas a palavra "auto"+espaço

cd /etc/wpa_supplicant/
sudo nano wpa_supplicant.conf

>adiciona os dados do access point do ardrone e deleta o resto
>>por exemplo:
network={
        ssid="ardrone_ufba"
        key_mgmt=NONE
}