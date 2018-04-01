import re
import random
import subprocess
a=subprocess.getoutput("ip addr")
log_line_re=re.compile(r'''inet (?P<ip>\s+\d+\.\d+\.\d+\.\d)+
''', re.VERBOSE)
def apacheconf(ip,dom_name,homedir):
    a='''<VirtualHost %s:80>
	ServerName %s
	ServerAlias www.%s
	DocumentRoot /var/www/%s
	ServerAdmin webmaster@test.com
	DirectoryIndex index.html index.php
	AddDefaultCharset off
	CustomLog /var/log/apache2/access.log combined
	ErrorLog /var/log/apache2/error.log
</VirtualHost>
<Directory /var/www/test.com >
	Options +Includes +ExecCGI
        allowoverride all
</Directory>''' % (ip,dom_name,dom_name,homedir)
    return a
def genstr():
    str1=[]
    strrange=range(ord('a'),ord('z')+1)
    for i in strrange:
        str1.append(chr(i))
#    for i in range(0,10):
#        str1.append(i)
    return ''.join(map(str,str1))

genst=genstr()
for i in log_line_re.findall(a):
    rd=random.randint(1,3)
    for b in range(0,rd):
        homedir = random.sample(genst, k=8)
        str_homerdir=''.join(homedir)
        domname= random.sample(genst,k=8)
        str_domname=''.join(domname)+"."+''.join(random.sample(genst, k=2))
        print(apacheconf(i,str_domname,str_homerdir))


