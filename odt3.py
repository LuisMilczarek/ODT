#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 15:16:47 2021

@author: luismilczarek
"""

'''
OBS:
    A biblioteca GUI esta sendo feita por mim
    
Anotações:
    tem como pegar posição atual do mouse sem click?
    a Entry fica selecionada o tempo todo, como habilitar somente no click?
'''
from gui import GuiApplication, Button, Container, InputText, Canvas, ColorIndicator, Label

# def saidaBotao(coord):
#     print("oi")

# def saidaContainer(coord):
#     print("toolbox")

class Application(GuiApplication):
    def __init__(self):
        super().__init__("ODT", 1280, 720)
        self.setBackgroundColor("#AAAAAA")
        
        self._fileName = "backup"
        
        self.toolPanel = Container(self._rootContainer, 10, 10, 200, 700) 
        # self.toolPanel.onClick = saidaContainer
        
        self.canvas = Canvas(self._rootContainer,220,10, 1050, 700)
        
        self.poligonBt = Button(self.toolPanel, 10, 10)
        self.poligonBt.onClick = self.setModePoligon
        self.poligonBt.text = "Poligono"
        
        self.rectangleBt = Button(self.toolPanel,10,40)
        self.rectangleBt.onClick = self.setModeRectangle
        self.rectangleBt.text = "Retangulo"
        
        
        self.circleBt = Button(self.toolPanel, 10, 70)
        self.circleBt.onClick = self.setModeCircle
        self.circleBt.text = "Circulo"
        
        self.ovalBt = Button(self.toolPanel, 10, 100)
        self.ovalBt.onClick = self.setModeOval
        self.ovalBt.text = "Oval"
        
        self.colorSelect = InputText(self.toolPanel, self.canvas.color, 10, 130)
        self.colorSelect.onEdit = self.setColor
        
        self.colorIndicator = ColorIndicator(self.toolPanel, 120, 130)
        self.colorIndicator.color = self.canvas.color
        
        self.colorLabel = Label(self.toolPanel, 150, 130, 40, 20)
        self.colorLabel.text = "Cor"
        
        self.borderColorSelect = InputText(self.toolPanel, self.canvas.borderColor, 10, 160)
        self.borderColorSelect.onEdit = self.setBorderColor
        
        self.borderColorIndicator = ColorIndicator(self.toolPanel, 120, 160)
        self.borderColorIndicator.color = self.canvas.borderColor
        
        self.borderColorLabel = Label(self.toolPanel, 150, 160, 40, 20)
        self.borderColorLabel.text = "Contorno"
        
        self.modeLabel = Label(self.toolPanel,10, 190, 100, 20)
        self.modeLabel.text = "Poligono"
        
        self.borderWidth = InputText(self.toolPanel, "Espessura", 10, 210)
        self.borderWidth.onEdit = self.setBorderWidth
        
        self.fileName = InputText(self.toolPanel, "Arquivo", 10, 240)
        self.fileName.onEdit = self.setFileName
        
        self.saveBt = Button(self.toolPanel, 10, 270)
        self.saveBt.onClick = lambda _: [self.canvas.saveDrawing(self._fileName)]
        self.saveBt.text = "Salvar"
        
        self.loadBt = Button(self.toolPanel, 10, 300)
        self.loadBt.onClick = lambda _: [self.canvas.openDrawing(self._fileName)]
        self.loadBt.text = "Carregar"
        
        self.credits = Label(self.toolPanel, 50, 675, 100, 20)
        self.credits.text = "Desenvolvido por Luís Milczarek"
        
    def setModeRectangle(self, _):
        self.canvas.setMode("Rectangle")
        self.modeLabel.text = "Retangulo"
    
    def setModePoligon(self, _):
        self.canvas.setMode("Poligon")
        self.modeLabel.text = "Poligono"
        # self.canvas.saveDrawing("data")
    
    def setModeCircle(self,_):
        self.canvas.setMode("Circle")
        self.modeLabel.text = "Circulo"
        
    def setModeOval(self,_):
        self.canvas.setMode("Oval")
        self.modeLabel.text = "Oval"
        # self.canvas.saveDrawing("")
        
    def setColor(self, text):
        text = text.upper()
        if text.startswith('#') and (len(text) == 4 or len(text) == 7) and all([c.isnumeric or ("A" <= c and c <= "F") for c in text]):
            self.canvas.color = text
            self.colorIndicator.color = text
        else:
            self.colorSelect.text = self.canvas.color
            
    def setBorderColor(self, text):
        text = text.upper()
        if text.startswith('#') and (len(text) == 4 or len(text) == 7) and all([c.isnumeric or ("A" <= c and c <= "F") for c in text]):
            self.canvas.borderColor = text
            self.borderColorIndicator.color = text
        else:
            self.borderColorSelect.text = self.canvas.color
            
    def setBorderWidth(self, width):
        if width.isnumeric():
            self.canvas.borderWidth = int(width)
        self.borderWidth.text = str(self.canvas.borderWidth)
    
    def setFileName(self, text):
        if text == "":
            self.fileName.text = "Arquivo"
        else:
            self._fileName = text
    
    def __del__(self):
        super().__del__()
        self.canvas.saveDrawing("backup")
        
if __name__ == "__main__":
    myApp = Application()
    myApp.run()
    myApp.stop()
    