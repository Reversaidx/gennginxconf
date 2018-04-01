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

virt_re=re.compile(r'''\n?\t?(.*)''' , re.VERBOSE )
print(virt_re.findall(test))

