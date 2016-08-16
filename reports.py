#!/usr/bin/python

import MySQLdb as mdb
import sys
import argparse
import datetime
import json
import pdfkit

web_host = "192.170.228.108"

parser = argparse.ArgumentParser(description='Availability reports for icingaweb2')
parser.add_argument('-g', '--hostgroup', type=str, help="Name of hostgroup")
parser.add_argument('-s', '--start', type=str, help="Start time for query yyyy-mm-dd hr:min:sec")
parser.add_argument('-e', '--end', type=str, help="End time for query yyyy-mm-dd hr:min:sec")
args = parser.parse_args()
group = args.hostgroup
start = args.start
end = args.end

now = datetime.datetime.now()
report_time = now.strftime("%Y-%m-%d-%T")

with open('dbaccess.json') as file:
    creds = json.load(file)
username = creds['credentials']['username']
password = creds['credentials']['password'] 
db = creds['credentials']['dbname']
host =  creds['credentials']['host']

count = 0

style = """
<style>
table, th, td {
   border: 1px solid black;
}
</style>
"""
try:


#Connect to mysql
    connect = mdb.connect(host,username,password,db);
    mysql = connect.cursor()
#Get hostgroup ID from name/alias

    #Build mysql query first then execute
    get_group_id = "select hostgroup_id from icinga_hostgroups where alias = '"+group+"'"
    mysql.execute(get_group_id)
    group_ids = mysql.fetchone()
    group_id = group_ids[0]
#Query hosts and calculate downtime averages

    #Build mysql query first then execute
    get_host_ids = "select host_object_id from icinga_hostgroup_members where hostgroup_id = "+str(group_id)
    mysql.execute(get_host_ids)
    hosts = [hosts[0] for hosts in mysql.fetchall()]
    total = 0

    report_name = report_time+"-"+group+".html"
    pdf_name = report_time+"-"+group+".pdf"

    with open('/var/www/html/reports/'+report_name,"a+") as file: 
        file.write("<!DOCTYPE html>\n")
        file.write("<html>\n")
        file.write("<head>\n")
        file.write(style+"\n")
        file.write("</head>\n")
        file.write("<body>\n")
        file.write("<h1 align=center >Report Date Range: "+str(start)+" - "+str(end)+"</h1>\n")
        file.write("<table align=center >\n")
        file.write("<tr style align=left> <th>Host Name</th> <th>Availability</th></tr>\n")

    for host in hosts:
        #Build mysql query first then execute
        get_availability = "select icinga_availability("+str(host)+","+str(start)+","+str(end)+")"
        get_display_names = "select display_name from icinga_hosts where host_object_id = "+str(host)
        mysql.execute(get_availability)
        results = mysql.fetchone()
        mysql.execute(get_display_names)
        host_name = mysql.fetchone()
        for result in results:
            with open('/var/www/html/reports/'+report_name, "a+") as file:
                file.write("<tr><td>{}</td> <td>{}</td></tr>\n" .format(host_name[0],result))
            total += result
            count += 1
    total_avail = total / count
    with open('/var/www/html/reports/'+report_name, "a+") as file:
        file.write("<tr><td>Total Hostgroup Availability = {}</td></tr>\n" .format(total_avail))
        file.write("</table>\n")
        file.write("</body>\n")
        file.write("</html>\n")

except mdb.Error, e:

    print "Error %d: %s " % (e.args[0], e.args[1])

    sys.ext(1)

finally:

    if connect:
        connect.close()

pdfkit.from_file('/var/www/html/reports/'+report_name, '/var/www/html/reports/'+pdf_name)
print "copy the following links: \n" 
print "HTML VIEW = "+web_host+"/reports/"+report_name
print "DOWNLOADABLE PDF= "+web_host+"/reports/"+pdf_name
