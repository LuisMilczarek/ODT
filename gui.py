#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 13:43:11 2021

@author: luismilczarek
"""

import graphics as gp
from math import pow, sqrt
import json

class GuiApplication(object):
    def __init__(self, title, width, height):
        self.win = gp.GraphWin(title, width, height)
        self.win.setCoords(0, height, width, 0)
        self._rootContainer = ClickArea(0, 0, width, height, self.win)
        self.lastActiveObj = self._rootContainer
        
        
        # self.retangulo_teste = gp.Rectangle(gp.Point(0, 0), gp.Point(100, 100))
        # self.retangulo_teste.setFill("#FFFFFF")
        # self.retangulo_teste.draw(self.win)
        
    
    def run(self):
        key = ""
        mouse = None
        while key != "Escape":
            key = self.win.checkKey()
            mouse = self.win.checkMouse()
            if key != "":
                print(f"Key:{key}")
                self.lastActiveObj.onKey(key)
            if mouse != None:                
                print(f"Mouse:{mouse}")
                self.lastActiveObj.onUnclick()
                self.lastActiveObj = self._rootContainer.clicked(mouse)
                
    def setBackgroundColor(self, color):
        self.win.setBackground(color)
    
    def stop(self):
        self.win.close()
        
    def __del__(self):
        self.stop()
    
class ClickArea(object):
    def __init__(self,x,y,w,h, win):
        
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.win = win
        self.objects = []
        
    def clicked(self, coord):
        for obj in self.objects:
            if obj.isClicked(coord):
                return obj.clicked(coord)
        self.onClick(coord)
        return self
    
    def onClick(self, coord):
        print(type(self))
        
    def onUnclick(self):
        pass
    
    def onKey(self, key):
        pass
    # def isClicked(self, coord):
    #     return coord[0] >= self.x and coord[0] <= self.x + self.width and coord[1] >= self.y and coord[1] <= self.y + self.height
    

class GuiObject(object):
    def __init__(self,parent, x, y, width, height):
        self.parent = parent
        self.win = parent.win
        self._topLeft = gp.Point(self.parent.x + x, self.parent.y + y)
        self._bottomRight = gp.Point(self._topLeft.getX() + width, self._topLeft.getY() + height)
        self._backgroundColor = "#FFFFFF"
        self.box = gp.Rectangle(self._topLeft, self._bottomRight)
        self.box.setFill(self._backgroundColor)
        self.box.draw(self.win)
        parent.objects += [self]
        self.objects = []
    
    @property
    def x(self):
        return self._topLeft.getX()
    
    @x.setter
    def x(self, value):
        self._topLeft.x = self.parent.x + value

    @property        
    def y(self):
        return self._topLeft.getY()
    
    @y.setter
    def y(self, value):
        self._topLeft.y = self.parent.y + value
    
    @property
    def width(self):
        return self._bottomRight.x - self._topLeft.x
    
    @width.setter
    def width(self, value):
        self._bottomRight.x = self._topLeft.x + value
        
    @property
    def height(self):
        return self._bottomRight.y - self._topLeft.y
        
    @height.setter
    def height(self, value):
        self._bottomRight.y = self._topLeft.y + value 
        
    def clicked(self, coord):
        for obj in self.objects:
            if obj.isClicked(coord):
                return obj.clicked(coord)
        self.onClick(coord)
        return self

    def onUnclick(self):
        pass
    
    def onClick(self, coord):
        print(type(self))
    
    def isClicked(self, coord):
        return coord.getX() >= self.x and coord.getX() <= self.x + self.width and coord.getY() >= self.y and coord.getY() <= self.y + self.height
    
    def onKey(self, key):
        pass

class Container(GuiObject):
    def __init__(self,parent, x, w, width, height):
        super().__init__(parent, x, w, width, height)
        

class Button(GuiObject):
    def __init__(self, parent, x, y, width=100, height=20):
        super().__init__(parent, x, y, width, height)
        self._text = gp.Text(self.box.getCenter(), "Button")
        self._text.draw(self.win)
        
    @property
    def text(self):
        return self._text.getText()

    @text.setter
    def text(self, value):
        # print(value)
        self._text.setText(value)
        
        
# class LineEdit(GuiObject):
#     def __init__(self,parent, x, y, width=100, height=20):
#         super().__init__(parent, x, y, width, height)
#         self._edit = gp.Entry(self.box.getCenter(), 10)
#         self._edit.draw(self.win)
        
class InputText(GuiObject):
    symbols = {
        "apostrophe":"'",
        "minus":'-',
        "equal":'=',
        "comma":',',
        "period":'.',
        "semicolon":";",
        "slash":"/",
        "KP_Divide":'/',
        "KP_Multiply":'*',
        "KP_Subtract":'-',
        "KP_Add":'+',
        "KP_Decimal":'.',
        "quotedbl":'"',
        "exclam":'!',
        "at":"@",
        "numbersign":'#',
        "dollar":'$',
        "percent":'%',
        "asterisk":'*',
        "parenleft":'(',
        "parenright":')',
        "underscore":'_',
        "plus":'+',
        "less":'<',
        "greater":'>',
        "colon":':',
        "question":'?',
        "bar":'|',
        "backslash":'\''
        }    
    def __init__(self, parent, text, x, y, width=100, height=20):
        super().__init__(parent, x, y, width, height)
        self._text = ""
        self._textObj = gp.Text(self.box.getCenter(), text)
        self._textObj.draw(self.win)
        
    def onClick(self, coord):
        self.text = ""
    
    def onUnclick(self):
        print(type(self._text))
        self.onEdit(self._text)
    
    def onKey(self, key):
        if key in self.symbols.keys():
            self._append(self.symbols[key])
        elif len(key) == 1:
            self._append(key)
        elif key == "Return" or key == "KP_Enter":
            print(type(self._text))
            self.onEdit(self._text)
        elif key.startswith("KP_"):
            self._append(key[-1])
        elif key == "BackSpace" and self._text != "":
            print("cheguei aqui")
            self.text = self._text[0:-1]

    def onEdit(self, text):
        pass
    
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        self._text = value
        self._textObj.setText(self._text)
    
    def _append(self, key):
        self._text += key
        self._textObj.setText(self._text)
        
class Label(GuiObject):
    def __init__(self, parent, x, y, width, height):
        super().__init__(parent, x, y, width, height)
        self._text = ""
        self._textObj = gp.Text(self.box.getCenter(), self._text)
        self.box.setOutline("#FFF")
        self._textObj.draw(self.win)
    
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        self._text = value
        self._textObj.setText(self._text)

class Canvas(GuiObject):
    def __init__(self, parent, x, y, width, height):
        super().__init__(parent, x, y, width, height)
        self.points = []
        self.lines = []
        self.drawings = []
        self._color = "#F00"
        self._borderColor = "#000"
        self._borderWidth = 1
        self.currentDrawingType = Poligon
        self.currentDrawing = self.currentDrawingType(self)
        self.currentDrawing.borderColor = self._borderColor
        self.currentDrawing.color = self._color
        self.drawingsTypes = {"Rectangle": Rectangle, 
                              "Poligon": Poligon, 
                              "Circle": Circle,
                              "Oval": Oval}
        
    def onClick(self, coord):
        # self.points.append(gp.Circle(coord, 5))
        # # self.points[-1].setWidth(12)
        # self.points[-1].setFill("#000")
        # self.points[-1].draw(self.win)
        
        # if len(self.points) > 1:
        #     self.lines.append(gp.Line(self.points[-2].getCenter(), self.points[-1].getCenter()))
        #     self.lines[-1].draw(self.win)
        self.currentDrawing.onClick(coord)
        if self.currentDrawing.isDone():
            self.drawings.append(self.currentDrawing.getDrawing())
            self.drawings[-1][0].draw(self.win)
            self.currentDrawing = self.currentDrawingType(self)
    
    def onKey(self, key):
        if key == "Delete" and len(self.drawings) > 0:
            self.drawings[-1][0].undraw()
            self.drawings.pop(-1)
        else:
            self.currentDrawing.onKey(key)
            if self.currentDrawing.isDone():
                self.drawings.append(self.currentDrawing.getDrawing())
                self.drawings[-1][0].draw(self.win)
                self.currentDrawing = self.currentDrawingType(self)
    
    def setMode(self, mode):
        self.currentDrawingType = self.drawingsTypes[mode]
        self.currentDrawing = self.currentDrawingType(self)
    
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, value):
        self._color = value
        self.currentDrawing.color = value
    
    @property
    def borderColor(self):
        return self._borderColor
    
    @borderColor.setter 
    def borderColor(self, value):
        self._borderColor = value
        self.currentDrawing.borderColor = value
        
    @property
    def borderWidth(self):
        return self._borderWidth
    
    @borderWidth.setter
    def borderWidth(self, value):
        self._borderWidth = value
        self.currentDrawing.width = self._borderWidth
        
    def saveDrawing(self, fileName):
        jsonObj = []
        for drawing in self.drawings:
            drawingDict = {}
            dType = type(drawing[0])
            print(drawing[0])
            if dType == gp.Polygon:
                drawingDict["type"] = "Poligon"
                drawingDict["points"] = [[p.getX(),p.getY()] for p in drawing[0].getPoints()]
            elif dType == gp.Rectangle:
                drawingDict["type"] = "Rectangle"
                p1 = drawing[0].getP1()
                p2 = drawing[0].getP2()
                drawingDict["points"] = [[p1.getX(),p1.getY()],[p2.getX(), p2.getY()]]
            elif dType == gp.Circle:
                drawingDict["type"] = "Circle"
                drawingDict["point"] = [drawing[0].getCenter().getX(), drawing[0].getCenter().getY()]
                drawingDict["radius"] = drawing[0].getRadius()
            elif dType == gp.Oval:
                drawingDict["type"] = "Oval"
                p1 = drawing[0].getP1()
                p2 = drawing[0].getP2()
                drawingDict["points"] = [[p1.getX(),p1.getY()],[p2.getX(), p2.getY()]]
            drawingDict["color"] = drawing[1]
            drawingDict["border"] = drawing[2]
            drawingDict["width"] = drawing[3]
            jsonObj.append(drawingDict)
        print(json.dumps(jsonObj))
        with open(f"{fileName}.json", "w") as f:
            json.dump(jsonObj, f)
            
    def openDrawing(self, fileName):
        jsonObj = None
        try:
            with open(f"{fileName}.json","r") as f:
                jsonObj = json.load(f)
            # print(jsonObj)
            for oldDrawing in self.drawings:
                oldDrawing[0].undraw()
            self.drawings= []
            for drawing in jsonObj:
                print(drawing)
                if drawing["type"] == "Poligon":
                    self.drawings.append([gp.Polygon([gp.Point(x, y) for (x,y) in drawing["points"]])])
                    print(self.drawings[-1])
                elif drawing["type"] == "Rectangle":
                    p1 = gp.Point(drawing["points"][0][0], drawing["points"][0][1])
                    p2 = gp.Point(drawing["points"][1][0], drawing["points"][1][1])
                    self.drawings.append([gp.Rectangle(p1, p2)])
                elif drawing["type"] == "Circle":
                    self.drawings.append([gp.Circle(gp.Point(drawing["point"][0], 
                                                            drawing["point"][1]),
                                                            drawing["radius"])])
                elif drawing["type"] == "Oval":
                    p1 = gp.Point(drawing["points"][0][0], drawing["points"][0][1])
                    p2 = gp.Point(drawing["points"][1][0], drawing["points"][1][1])
                    self.drawings.append([gp.Oval(p1, p2)])
                self.drawings[-1][0].setFill(drawing["color"])
                print("1")
                self.drawings[-1].append(drawing["color"])
                print("2")
                self.drawings[-1][0].setOutline(drawing["border"])
                self.drawings[-1].append(drawing["border"])
                self.drawings[-1][0].setWidth(drawing["width"])
                self.drawings[-1].append(drawing["width"])
                self.drawings[-1][0].draw(self.win)
        except Exception as e:
            print(f"[ERROR][FILE] {e}")
            
class ColorIndicator(GuiObject):
    def __init__(self, parent, x, y, width=20, height=20):
        super().__init__(parent, x, y, width, height)
        self._color = "#000"

    @property        
    def color(self):
        return self._color 
    
    @color.setter
    def color(self, value):
        self._color = value
        self.box.setFill(self._color)
        # print(color)
        
class DrawingObject(object):
    def __init__(self, parent):
        self.win = parent.win
        self.points = []
        self.color = parent.color
        self.borderColor = parent.borderColor
        self.width = parent.borderWidth
        
    def onClick(self, coord):
        pass
    
    def onKey(self, key):
      pass
  
    def isDone(self):
        pass
    
    def getDrawing(self):
        pass
    
    def __del__(self):
        for point in self.points:
            point.undraw()
        
class Poligon(DrawingObject):
    def __init__(self, parent):
        super().__init__(parent)
        self.lines = []
        self._done = False
        
    
    def onClick(self, coord):
        if not self._done:
            self.points.append(gp.Circle(coord, 2.5))
            # self.points[-1].setWidth(12)
            self.points[-1].setFill("#000")
            self.points[-1].draw(self.win)
            
            if len(self.points) > 1:
                self.lines.append(gp.Line(self.points[-2].getCenter(), self.points[-1].getCenter()))
                self.lines[-1].draw(self.win)
            
    def onKey(self,key):
        if key == "BackSpace" and not self._done:
            if len(self.points) >= 2:
                self.lines[-1].undraw()
                self.points[-1].undraw()
                print(self.lines.pop(-1))
                print(self.points.pop(-1))
            elif len(self.points) > 0:
                self.points[0].undraw()
                self.points.pop(0)
        elif key == "space":
            self.lines.append(gp.Line(self.points[-1].getCenter(), self.points[0].getCenter()))
            self.lines[-1].draw(self.win)
            self._done = True
    
    def isDone(self):
        return self._done
    
    def getDrawing(self):
        # for line in self.lines:
        #     line.undraw()
            
        # for point in self.points:
        #     point.undraw()
        drawing = gp.Polygon([point.getCenter() for point in self.points])
        drawing.setFill(self.color)
        drawing.setOutline(self.borderColor)
        drawing.setWidth(self.width)
        return [drawing, self.color, self.borderColor, self.width]
        
            
    def __del__(self):
        super().__del__()
        for line in self.lines:
            line.undraw()
            
class Rectangle(DrawingObject):
    def __init__(self, parent):
        super().__init__(parent)
        self._done = False
        
    def onClick(self, coord):
        if len(self.points) <= 2:
            self.points.append(gp.Circle(coord, 2.5))
            self.points[-1].setFill("#000")
            self.points[-1].draw(self.win)
            if len(self.points) == 2:
                self._done = True
                
    def isDone(self):
        return self._done
    
    def getDrawing(self):
        drawing = gp.Rectangle(self.points[0].getCenter(), self.points[1].getCenter())
        drawing.setFill(self.color)
        drawing.setOutline(self.borderColor)
        drawing.setWidth(self.width)
        return [drawing, self.color, self.borderColor, self.width]


class Circle(DrawingObject):
    def __init__(self, parent):
        super().__init__(parent)
        self._done = False
        
    def onClick(self, coord):
        if len(self.points) <= 2:
            self.points.append(gp.Circle(coord, 2.5))
            self.points[-1].setFill("#000")
            self.points[-1].draw(self.win)
            if len(self.points) == 2:
                self._done = True
                
    def isDone(self):
        return self._done
    
    def getDrawing(self):
        radius = sqrt(pow((self.points[0].getCenter().getX() - self.points[1].getCenter().getX()),2)\
            + pow(self.points[0].getCenter().getY() -self.points[1].getCenter().getY(),2))
        drawing = gp.Circle(self.points[0].getCenter(),
                            radius)
        drawing.setFill(self.color)
        drawing.setOutline(self.borderColor)
        drawing.setWidth(self.width)
        return [drawing, self.color, self.borderColor, self.width]


class Oval(DrawingObject):
    def __init__(self, parent):
        super().__init__(parent)
        self._done = False
        
    def onClick(self, coord):
        if len(self.points) <= 2:
            self.points.append(gp.Circle(coord, 2.5))
            self.points[-1].setFill("#000")
            self.points[-1].draw(self.win)
            if len(self.points) == 2:
                self._done = True
                
    def isDone(self):
        return self._done
    
    def getDrawing(self):
        drawing = gp.Oval(self.points[0].getCenter(), self.points[1].getCenter())
        drawing.setFill(self.color)
        drawing.setOutline(self.borderColor)
        drawing.setWidth(self.width)
        return [drawing, self.color, self.borderColor, self.width]
