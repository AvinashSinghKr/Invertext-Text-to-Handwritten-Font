from PIL import Image, ImageDraw, ImageFont
import random
from fpdf import FPDF
import os

pdf = FPDF()

class gen:
	lastchar=0
	imagelist=[]

obj=gen()

dir='C:/Users/Devansh/Desktop/paper/text to handwritten'

def makepdf(filename,imagelist,pageno):
	for img in imagelist:
		pdf.add_page()
		pdf.image(img,x=0,y=0,w=210,h=297)
	pdf.output(filename,"F")

	for img in imagelist:
		os.remove(img)

	if(pageno != 0):
		for i in range(pageno):
			os.remove(dir+"/temp/formattedtext{}.txt".format(i))
	else:
		os.remove(dir+"/temp/formattedtext{}.txt".format(pageno))

def generate(pageno):
	
	#opening background images and selecting a random image from them
	image1 = Image.open(dir+'/backgrounds/01.jpg')
	image2 = Image.open(dir+'/backgrounds/02.jpg')
	image3 = Image.open(dir+'/backgrounds/03.jpg')
	image = random.choice([image1,image2,image3])
	draw = ImageDraw.Draw(image)

	#initialising font variables with different fonts
	font_type_1 = ImageFont.truetype(dir+'/font/Messycircles-Regular.ttf',72)
	font_type_2 = ImageFont.truetype(dir+'/font/Messycircles2-Regular.ttf',72)
	font_type_3 = ImageFont.truetype(dir+'/font/Messycircles3-Regular.ttf',72)
	font_type_4 = ImageFont.truetype(dir+'/font/Messycircles4-Regular.ttf',72)

	#opening the formatted user input file to read
	ifile = open(dir+'/temp/input.txt','r')

	#creating a new file to write text in specific format
	ofile = open(dir+'/temp/formattedtext{}.txt'.format(pageno),'w')

	data = ifile.read()
	ifile.close()

	character_count=0 #character counter
	l=0 #line counter

	#writing in the newly created file
	if(pageno==0):
		for i in range(0, len(data)):
			if(l<23):
				ofile.write(data[i])
				character_count += 1
				if(character_count>48 and data[i]==' '):
					ofile.write('\n')
					l += 1
					character_count = 0
				if(data[i]=='\n'):
					ofile.write('\n')
					character_count = 0
					l += 1
			else:
				obj.lastchar=i
				break

	else:
		for i in range(obj.lastchar, len(data)):
			if(l<23):
				ofile.write(data[i])
				character_count+=1
				if(character_count>48 and data[i]==' '):
					ofile.write('\n')
					character_count = 0
					l += 1
				if(data[i]=='\n'):
					ofile.write('\n')
					character_count = 0
					l += 1
			else:
				obj.lastchar=i
				break

	ofile.close()
	ofile = open(dir+'/temp/formattedtext{}.txt'.format(pageno),'r')
	lines = ofile.readlines()
	ofile.close()

	#coordinates for lines
	x_cord = list(range(135,160))
	y_cord = list(range(125,130))

	#setting y coordinate for the first line
	y_value=190

	lineno=0 #line counter

	for line in lines:
		#choosing a random font
		font = random.choice([font_type_1,font_type_2,font_type_3,font_type_4])

		#generating random x coordinates
		x_value = random.choice(x_cord)

		#writing text on background image
		draw.text(xy=(x_value,y_value),text=line,fill='#414f8c',font=font)
		
		#incrementing y_value
		if(line=='\n'):
			y_value=y_value+50
		else:
			y_value=y_value+random.choice(y_cord)

	image.save(dir+"/temp/{}.jpg".format(pageno))
	filename=dir+"/temp/{}.jpg".format(pageno)
	obj.imagelist.append(filename)


def main():
	import math

	#opening 
	f = open(dir+'/temp/input.txt','r')
	data=f.read()
	f.close()

	f1 = open(dir+'/temp/formattedtextbasic.txt','w')

	ch=0 #character counter

	for i in range(0, len(data)):
		f1.write(data[i])
		ch=ch+1
		if(ch>48 and data[i]==' '):
			f1.write('\n')
			ch=0
		if(data[i]=='\n'):
			f1.write('\n')
			ch=0

	f1.close()
	f1 = open(dir+'/temp/formattedtextbasic.txt','r')
	lines=f1.readlines()
	f1.close()

	pageno=0
	no_of_lines = 0

	for line in lines:
		no_of_lines = no_of_lines+1

	if(no_of_lines > 23):
		for i in range(round(no_of_lines / 22)):
			generate(pageno)
			pageno = pageno + 1
	else:
		generate(pageno)

	os.remove(dir+"/temp/formattedtextbasic.txt")

	makepdf("handwrittenfile.pdf",obj.imagelist,pageno)

	pageno = 0
	n=no_of_lines
	for i in range(no_of_lines):
		if(n>23):
			pageno=pageno+1
			n+=1