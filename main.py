import webbrowser as wb
import requests as rq
import tempfile as tmpf
import re as re

def clean_html(raw_html):
    cleanr=re.compile('<.*?>')
    cleantext=re.sub(cleanr,'',raw_html)
    return cleantext

def main():
    id_rep=91
    lang="en_EN"
    usr="NjEzYTMxM2E3YjY5M2EzMDNiNzMzYTM0M2EyMjc0NjU3Mzc0MjIzYjdk"
    params="&nprm[]=prm_name1&vprm[]=prm_value1&nprm[]=prm_name2&vprm[]=prm_value2"

    content=rq.get("http://127.0.0.1:8080/rep/rep_internal.php?id_rep="+str(id_rep)+"&outf=T&login="+usr+"&lg="+lang+"&hdr=T&delf=T"+params)
	# outf=T - we receive from ProReports report file (type of file in Content-Type header)
	# delf=T - report file is deleted on server side 
	# lg=en_EN - language of messages (if error occured) 
	# hdr=T - if error occured in response is setting HTTP header with number of error code
	# params - this we can ignore if report haven't parameters

    if (content.status_code == 200):
        ftype=content.headers["Content-Type"]
        ltype=ftype.split(sep=";",maxsplit=2)
        ltype=ltype[0].split(sep="/",maxsplit=2)
        tf=tmpf.NamedTemporaryFile(suffix="."+ltype[1],delete=False)
        tf.write(content.content)
        wb.open("file://"+tf.name)
    else:
        print("Error occured: "+str(content.status_code)+" : "+ clean_html(content.content.decode()))

if __name__ == "__main__":
    main()