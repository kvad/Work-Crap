#!/usr/bin/env python
#
#createTiretrack.py
#
#@author 	kurtis
#@date:		11/03/09
#
#Make those lame tiretrack pages from vb files will be upgraded soon
#works for now ............

import sys, os 
from cStringIO import StringIO
OUTFILE = "track_garage.php"	#output page

def addContent(tag):
	'''Insert Tire track Tag with an iframe'''

	track_tag = """<!-- begin content -->
<table align="center" border="0" cellpadding="6" cellspacing="1"
class="tborder" width="100%">
        <tr>
                <td class="tcat"><span class="smallfont"><strong>The Tire
Rack Upgrade Garage</strong></span></td>
        </tr>
        <tr>

                <td class="alt2">
            <IFRAME
SRC=\'"""+ tag + """\'
TITLE="The Tire Rack Upgrade Garage" WIDTH="100%" HEIGHT="600"
scrolling="no"
class="tborder">
            </IFRAME>

        </td>
</tr>
</table>

<!-- End Content -->

"""
	res = StringIO(track_tag)
	return res

def check_args():
	'''Make sure that we have a file to open and a tiretrack ad code'''
	if len(sys.argv) <> 3:
        	print "error <html_page> <add_code>"
        	sys.exit(1)
		
def checkFile(file):
	'''Delete file from current directory'''
	listDir = os.listdir('.')
	if file in listDir:
		os.remove(file)

def main():
	'''Main execution of program'''
	f = sys.argv[1]		#for now the input is a file object :(
	tire_tag = sys.argv[2]  #Tag from marketing :(
	page = open(f,'r').readlines()
	checkFile(OUTFILE)		#make sure we start fresh
	outfile = open(OUTFILE,'w')	#file handler for our new page

	#Get the Heading of the page and stop before the nav bar is throw in
	for line in page:
		res = line.find('<!-- content table -->')
		if res != -1:
			outfile.writelines(line)
			break
		outfile.writelines(line)


	res = addContent(tire_tag).read()       #grap the tag code  
	outfile.write(res)			#write to the file

	IN_CONTENT = False			#Find the footer of the page

	for line in page:
		if IN_CONTENT == True:
			outfile.writelines(line)
		res = line.find('<!-- /content area table -->')
		if res != -1:
			IN_CONTENT = True	#When we find the footer write the rest	

	outfile.close()

if __name__ == '__main__':
	check_args()
	main()
