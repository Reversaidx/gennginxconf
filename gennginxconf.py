# -*- coding: utf-8 -*-
import os,re,subprocess,shutil
test='''<VirtualHost  192.168.0.116:80>
	ServerName cdugxlpj.mk
	ServerAlias www.cdugxlpj.mk
	DocumentRoot /var/www/phkdnbam
	ServerAdmin webmaster@test.com
	DirectoryIndex index.html index.php
	AddDefaultCharset off
	CustomLog /var/log/apache2/access.log combined
	ErrorLog /var/log/apache2/error.log
</VirtualHost>
<Directory /var/www/test.com >
	Options +Includes +ExecCGI
        allowoverride all
</Directory>
<VirtualHost  192.168.0.116:80>
	ServerName ceqjbtgz.xh
	ServerAlias www.ceqjbtgz.xh
	DocumentRoot /var/www/kayiolgm
	ServerAdmin webmaster@test.com
	DirectoryIndex index.html index.php
	AddDefaultCharset off
	CustomLog /var/log/apache2/access.log combined
	ErrorLog /var/log/apache2/error.log
</VirtualHost>
<Directory /var/www/test.com >
	Options +Includes +ExecCGI
        allowoverride all
</Directory>
<VirtualHost  192.168.0.116:443>
	ServerName ceqjbtgz.xh
	ServerAlias www.ceqjbtgz.xh
	SSLEngine on
    SSLCertificateFile /path/to/your_domain_name.crt
    SSLCertificateKeyFile /path/to/your_private.key
    SSLCertificateChainFile /path/to/DigiCertCA.crt
	DocumentRoot /var/www/kayiolgm.ru
	ServerAdmin webmaster@test.com
	DirectoryIndex index.html index.php
	AddDefaultCharset off
	CustomLog /var/log/apache2/access.log combined
	ErrorLog /var/log/apache2/error.log
</VirtualHost>
<Directory /var/www/test.com >
	Options +Includes +ExecCGI
        allowoverride all
</Directory>'''
test2='''
127.0.0.1:8080         is a NameVirtualHost
         default server domttest.ru (/etc/httpd/conf/vhosts/domttest/domttest.ru:2)
         port 8080 namevhost domttest.ru (/etc/httpd/conf/vhosts/domttest/domttest.ru:2)
                 alias www.domttest.ru
         port 8080 namevhost bitest.domttest.ru (/etc/httpd/conf/vhosts/domttest/bitest.domttest.ru:2)
                 alias www.bitest.domttest.ru
         port 8080 namevhost bitest2.domttest.ru (/etc/httpd/conf/vhosts/domttest/bitest2.domttest.ru:2)
                 alias www.bitest2.domttest.ru
         port 8080 namevhost esbit.domttest.ru (/etc/httpd/conf/vhosts/domttest/esbit.domttest.ru:2)
                 alias www.esbit.domttest.ru
         port 8080 namevhost mail.domttest.ru (/etc/httpd/conf/vhosts/domttest/mail.domttest.ru:2)
                 alias www.mail.domttest.ru
'''
#Класс в котором хранятся параметры virtual host
class virt_host():
    def __init__(self, servername , port):
        self.servername=servername
        self.port=port
    def add(self,serveralias,serverroot,serverip,serverindex):
        self.serveralias=serveralias
        self.serverroot=serverroot
        self.serverip=serverip
        self.serverindex=serverindex
    def addcert(self,cert,key,chain):
        self.cert=cert
        self.key=key
        self.chain=chain
#Заполнение класса virt_host и генерация конфига
def gennginx():
    virt_re = re.compile(r'''(?P<virthost><VirtualHost .*>[\s\S]*?</VirtualHost>)''', re.VERBOSE)
    hosts = virt_re.findall(config)
    servername_re = re.compile(r'''ServerName\s+(\S*)\s?''', re.IGNORECASE)
    serveralias_re = re.compile(r'''ServerAlias\s+(.*)''', re.IGNORECASE)
    serverroot = re.compile(r'''DocumentRoot\s+(.*)''', re.IGNORECASE)
    serverip = re.compile(r'''<VirtualHost\s+(.*):\d+''', re.IGNORECASE)
    serverport = re.compile(r'''<VirtualHost\s+.*:(\d+)''', re.IGNORECASE)
    serverindex = re.compile(r'''DirectoryIndex\s+(.*)''', re.IGNORECASE)
    servercert = re.compile(r'''SSLCertificateFile\s+(.*)''', re.IGNORECASE)
    serverkey = re.compile(r'''SSLCertificateKeyFile\s+(.*)''', re.IGNORECASE)
    serverchain=re.compile(r'''SSLCertificateChainFile\s+(.*)''',  re.IGNORECASE)
    list = []
    for i in hosts:
        virt_host_name = servername_re.findall(i)
        list.append(virt_host(virt_host_name, serverport.findall(i)[0]))
        try:
          virt_host.add(list[-1], serveralias_re.findall(i)[0], serverroot.findall(i)[0], serverip.findall(i)[0], serverindex.findall(i)[0])
          if int(list[-1].port) == 443:
            virt_host.addcert(list[-1], servercert.findall(i)[0], serverkey.findall(i)[0],serverchain.findall(i)[0])
        except:
          pass
    for i in list:
       try:

        if int(i.port) == 80:
            file = open(i.servername[0] + ".conf", 'wt')
            file.write('''server {
 	server_name %s %s;
 	charset off;
 	index %s;
 	disable_symlinks if_not_owner from=$root_path;
 	access_log /var/log/nginx/access.log;
 	error_log /var/log/nginx/error.log notice;
 	ssi on;
 	set $root_path %s;
 	root $root_path;
 	listen %s:80;
 	Strict-Transport-Security;

 	location / {
 		location ~ [^/]\.ph(p\d*|tml)$ {
 			try_files /does_not_exists @fallback;
 		}
 		location ~* ^.+\.(jpg|jpeg|gif|png|svg|js|css|mp3|ogg|mpe?g|avi|zip|gz|bz2?|rar|swf)$ {
 			try_files $uri $uri/ @fallback;
 		}
 		location / {
 			try_files /does_not_exists @fallback;
 		}
 	}
 	location @fallback {
 		proxy_pass http://127.0.0.1:8080;
 		proxy_redirect http://127.0.0.1:8080 /;
 		proxy_set_header Host $host;
 		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
 		proxy_set_header X-Forwarded-Proto $scheme;
 		proxy_set_header X-Forwarded-Port $server_port;
 		access_log off;
 	}
 }''' % (i.servername[0], i.serveralias, i.serverindex, i.serverroot, i.serverip))

        if int(i.port) == 443:
            subprocess.call("cat %s %s >%s.bundle" %(i.cert,i.chain,i.cert),shell=True)
            file = open(i.servername[0] + "ssl.conf", "wt")
            file.write('''server {
 	server_name %s %s;
 	ssl on;
 	ssl_certificate "%s.bundle";
 	ssl_certificate_key "%s";
 	ssl_ciphers EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH;
 	ssl_prefer_server_ciphers on;
 	ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
 	add_header Strict-Transport-Security "max-age=31536000;";
 	ssl_dhparam /etc/ssl/certs/dhparam4096.pem;
 	charset off;
 	index %s;
 	disable_symlinks if_not_owner from=$root_path;
 	access_log /var/log/nginx/aceess.log;
 	error_log /var/log/nginx/aceess.log notice;
 	ssi on;
 	set $root_path %s;
 	root $root_path;
 	listen %s:443;
 	location / {
 		location ~ [^/]\.ph(p\d*|tml)$ {
 			try_files /does_not_exists @fallback;
 		}
 		location ~* ^.+\.(jpg|jpeg|gif|png|svg|js|css|mp3|ogg|mpe?g|avi|zip|gz|bz2?|rar|swf)$ {
 			try_files $uri $uri/ @fallback;
 		}
 		location / {
 			try_files /does_not_exists @fallback;
 		}
 	}
 	location @fallback {
 		proxy_pass http://127.0.0.1:8080;
 		proxy_redirect http://127.0.0.1:8080 /;
 		proxy_set_header Host $host;
 		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
 		proxy_set_header X-Forwarded-Proto $scheme;
 		proxy_set_header X-Forwarded-Port $server_port;
 		access_log off;
 	}
 }''' % (i.servername[0], i.serveralias, i.cert, i.key, i.serverindex, i.serverroot, i.serverip))
       except:
        pass 
#Получаем список файлов в котором хранятся виртуальные хосты, и генерим общий конфиг который будем в будующем парсить
def changeapacheconf():
#Бекапим конфиги
    serverip = re.compile(r'''<VirtualHost\s+(\d+\.\d+\.\d+\.\d+):.*''', re.IGNORECASE)
    ip=serverip.findall(config)

    if not os.path.isdir("/root/backup"):
        os.mkdir("/root/backup")
    for i in files:
     shutil.copy(i,"/root/backup")
#    for i in files:
#        serverip.sub(test)
    for ip in ip:
     for i in files:
      subprocess.call("sed -i 's/%s:80/127.0.0.1:8080/g' %s" %(ip,i),shell=True)
      subprocess.call("sed -i 's/%s:443/127.0.0.1:8080/g' %s" %(ip,i),shell=True)



def readconfig():
    global config,files,config2
    apachectl=subprocess.getoutput("apachectl -S")
    path = re.compile(r'''\((.*):\d+\)''', re.IGNORECASE)
    files = list(set(path.findall(apachectl))) #Получаем только уникальные значения путей
    config2 = []
    for i in files:
        file = open(i, 'rt')
        config2 += file.readlines()
    config=''.join(config2)	
if __name__ == '__main__':
   readconfig()
   gennginx()
   changeapacheconf()


