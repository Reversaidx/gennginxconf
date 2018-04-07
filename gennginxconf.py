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
     virt_host.add(list[-1],serveralias_re.findall(i),serverroot.findall(i),serverip.findall(i),serverindex.findall(i))

print (list[0].servername,list[0].serverroot)




