# icingaweb2_availability_reports 0.1
python reporting module for icinga web 2

Not even close to completed....

Requires pdfkit: https://pypi.python.org/pypi/pdfkit

Use the below to install wkhtmltopdf:

'''
sudo apt-get install xfonts-75dpi
wget http://download.gna.org/wkhtmltopdf/0.12/0.12.2/wkhtmltox-0.12.2_linux-trusty-amd64.deb
sudo dpkg -i wkhtmltox-0.12.2_linux-trusty-amd64.deb
wkhtmltopdf http://www.google.com test.pdf
'''

Uses the icinga_reports_1.10.0 SQL function found here: https://github.com/Icinga/icinga-reports/releases

This must be installed and working before this script will function. 



version 0.1 
- accepts flags for hostgroup name, start and end time for availability reports. 
- Will calculate downtime for group and individual hosts then print to very basic html file. 
- pdfkit used to convert .html to .pdf
