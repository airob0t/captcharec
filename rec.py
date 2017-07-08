#coding:utf-8

import pytesseract
from PIL import Image,ImageFile,ImageEnhance
import subprocess
ImageFile.LOAD_TRUNCATED_IMAGES = True

def process(filename):    #处理图片  
    img=Image.open(filename)  
    enhancer=ImageEnhance.Color(img)  
    enhancer=enhancer.enhance(0)   #变成黑白  
    enhancer=ImageEnhance.Brightness(enhancer) #这下面的参数是经过测试后图片效果最好的。。。  
    enhancer=enhancer.enhance(2)   #提高亮度  
    enhancer=ImageEnhance.Contrast(enhancer)  
    enhancer=enhancer.enhance(8)   #提高对比度  
    #enhancer=ImageEnhance.Sharpness(enhancer)  
    #enhancer=enhancer.enhance(20)  #锐化  
    return enhancer  
  
def delims(image,numbers=4,rect=()):    #分割  
    ''' 
        image为图片, 
        numbers为图片上验证码的个数, 
        rect为要切割的矩形元组,有4个值,为左上右下 
    ''' 
    if len(rect):                               #图片会被处理成一定的大小再进行切割  
        image=image.crop((rect))  
    width,height=image.size  
    for i in range(numbers):  
        img=image.crop((int(width/numbers)*i,0,int(width/numbers)*(i+1),height))  
        img.save('./temp/%d.png' % i)  

def rec(imagename,num=0):
    code = ''
    if num==0:
        image = Image.open(imagename)
        imagename = imagename[:imagename.rfind('.')]+'.png'
        image.save(imagename)
        subprocess.call('tesseract '+imagename+' result -psm 7 digits')
        with open('result.txt','r') as f:
            code = f.read().strip().replace(' ','')
    else:
        image = process(imagename)
        delims(image,num)
        for i in xrange(num):
            p = subprocess.call('tesseract ./temp/%d.png result -psm 10 digits' % i)
            with open('result.txt') as f:
                code += f.read().strip()
    return code
#print rec('getcode.gif')
