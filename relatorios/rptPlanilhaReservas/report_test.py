#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 15:32:07 2020

@author: alexandre
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.colors import pink, black, red, blue, green, grey, white
from reportlab.lib.units import inch, mm

def hello(c):
   #cabecalho
   c.setFillColorRGB(0,0,0)
   c.rect(10*mm,266*mm,90*mm,10*mm, stroke=1 ,fill=1)
   c.setFillColor(white)
   c.setFont("Courier-Bold", 14)
   c.drawString(15*mm,269.5*mm,"Titulo 1")
   c.drawString(55*mm,269.5*mm,"Titulo 2")
   c.setFillColor(black)
   #c.grid([10*mm, 50*mm, 100*mm], [276*mm, 266*mm])
   #c.setFillColor(white)
   #Lista
   # define a large font
   c.setFont("Helvetica", 10)
   c.drawString(15*mm,282*mm,"Hello World")
   linhas = [266*mm]
   for x in range(20):
       c.drawString(15*mm,(261*mm)-(x*6*mm),"Linha "+str(x))
       c.drawString(55*mm,(261*mm)-(x*6*mm),"Linha "+str(x)+" Coluna 2")
       linhas.append((260*mm)-(x*6*mm)-2)
   c.setStrokeColor(grey)
   c.grid([10*mm, 50*mm, 100*mm], linhas)
   c.setStrokeColor(black)
   
c = canvas.Canvas('myfile.pdf', pagesize=A4)
hello(c)
c.showPage()
c.save()