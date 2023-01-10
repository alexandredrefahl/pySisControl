#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 16:47:23 2020

@author: alexandre
"""

from PyQt5 import QtCore, QtWidgets, QtSql
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.colors import pink, black, red, blue, green, grey, white
from reportlab.lib.units import inch, mm
import os



def monta_pagina(c):
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



if __name__ == '__main__':
   biblioteca
   print("Passou aqui")
   query = QtSql.QSqlQuery(db)
   is_valid_query = query.prepare("SELECT id,Cientifico,Popular FROM Mercadoria ORDER BY id")
   #is_valid_query = query.prepare("SELECT * FROM credentials WHERE username = ? and password = ?")
   # Query com parametros
   if is_valid_query:
      #query.addBindValue(username)
      #query.addBindValue(password)
      if query.exec_():
         c = canvas.Canvas('report.pdf', pagesize=A4)
         monta_pagina(c)
         linhas = [266*mm]
         x=0
         while query.next():
            print(query.value(0), " ", query.value(1), " ", query.value(2))
            c.setFont("Helvetica", 10)
            c.drawString(15*mm,(261*mm)-(x*6*mm),str(query.value(0)))
            c.drawString(55*mm,(261*mm)-(x*6*mm),query.value(1))
            c.drawString(103*mm,(261*mm)-(x*6*mm),query.value(1))
            linhas.append((260*mm)-(x*6*mm)-2)
            c.setStrokeColor(grey)
            x+=1
         c.grid([10*mm, 50*mm, 100*mm, 133*mm], linhas)
         c.setStrokeColor(black)
         c.showPage()
         c.drawString(20*mm,280*mm,"Segunda Pagina")
         c.showPage()
         c.drawString(20*mm,280*mm,"Terceira Pagina")
         c.save()
         os.system("xdg-open report.pdf")
      else:
         print('Failed')
   else:
      print(query.lastError().text())
   db.close()