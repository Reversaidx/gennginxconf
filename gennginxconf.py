import os,re,subprocess
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
</Directory>'''


class virt_host():
    def __init__(self, servername):
        self.servername=servername
    def add(self,serveralias,serverroot,serverip,serverindex):
        self.serveralias=serveralias
        self.serverroot=serverroot
        self.serverip=serverip
        self.serverindex=serverindex


if __name__ == '__main__':
 virt_re=re.compile(r'''(?P<virthost><VirtualHost .*>[\s\S]*?</VirtualHost>)''' , re.VERBOSE )
 hosts=virt_re.findall(test)
 servername_re=re.compile(r'''ServerName\s+(.*)''',re.IGNORECASE)
 serveralias_re=re.compile(r'''ServerAlias\s+(.*)''',re.IGNORECASE)
 serverroot=re.compile(r'''DocumentRoot\s+(.*)''',re.IGNORECASE)
 serverip=re.compile(r'''<VirtualHost\s+(.*):\d+''',re.IGNORECASE)
 serverindex=re.compile(r'''DirectoryIndex\s+(.*)''',re.IGNORECASE)
 list=[]
 for i in hosts:
     virt_host_name=servername_re.findall(i)
     list.append(virt_host(virt_host_name))
     virt_host.add(list[-1],serveralias_re.findall(i)[0],serverroot.findall(i)[0],serverip.findall(i)[0],serverindex.findall(i)[0])

 for i in list:
     file=open(i.servername[0]+".conf",'wt')
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
}''' %(i.servername[0],i.serveralias,i.serverindex,i.serverroot,i.serverip,))




