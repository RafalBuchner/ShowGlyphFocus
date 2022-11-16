# encoding: utf-8
from __future__ import division, print_function, unicode_literals

###########################################################################################################
#
#
#	Reporter Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
from AppKit import NSPoint, NSAffineTransform, NSAffineTransformStruct, NSRect, NSColor, NSBezierPath
import math
from vanilla import Window, Group, TextBox, CheckBox

	


class ShowGlyphFocus(ReporterPlugin):

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'Glyph Focus', 
			'de': 'Fokus auf aktuelle Glyphe',
			'fr': 'focus sur le glyphe actuel',
			'es': 'concentración en el glifo actual',
		})
		self.LoadPreferences()

		viewWidth = 200
		viewHeight = 140
		self.contextualMenuView = Window((viewWidth, viewHeight))
		self.contextualMenuView.group = Group((0, 0, viewWidth, viewHeight))
		self.contextualMenuView.group.text = TextBox((10, 10, -10, -10), "Show Glyph Focus")#, callback=self.checkboxCallback)
		self.contextualMenuView.group.showHighlight = CheckBox((10, 0, -10, -10), "show highlight", callback=self.checkboxCallback, value=self.showHighlight)
		self.contextualMenuView.group.showRSB = CheckBox((10, 40, -10, -10), "show RSB", callback=self.checkboxCallback, value=self.showRSB)
		self.contextualMenuView.group.showTriangle = CheckBox((10, 80, -10, -10), "show triangles", callback=self.checkboxCallback, value=self.showTriangle)
		self.contextualMenuView.group.showWhileMetrics = CheckBox((10, 120, -10, -10), "work on Show Metrics", callback=self.checkboxCallback, value=self.showWhileMetrics)
		
		
		self.generalContextMenus = [
			{"view": self.contextualMenuView.group.getNSView()}
		]

	@objc.python_method
	def checkboxCallback(self, sender):
		if sender.getTitle() == "show highlight":
			self.showHighlight = True if sender.get() else False
		if sender.getTitle() == "show RSB":
			self.showRSB = True if sender.get() else False
		if sender.getTitle() == "show triangles":
			self.showTriangle = True if sender.get() else False
		if sender.getTitle() == "work on Show Metrics":
			self.showWhileMetrics = True if sender.get() else False
		Glyphs.font.currentTab.redraw()
		self.SavePreferences()

	@objc.python_method
	def conditionsAreMetForDrawing(self):
		"""
		Only activate if text or pan (hand) tool are active.
		"""
		currentController = self.controller.view().window().windowController()
		if currentController:
			tool = currentController.toolDrawDelegate()
			textToolIsActive = tool.isKindOfClass_( NSClassFromString("GlyphsToolText") )
			if textToolIsActive: 
				return True
		return False

	@objc.python_method
	def SavePreferences( self):
		try:
			# write current settings into prefs:
			Glyphs.defaults["com.mekkablue.ShowGlyphFocus.showHighlight"] = self.showHighlight
			Glyphs.defaults["com.mekkablue.ShowGlyphFocus.showRSB"] = self.showRSB
			Glyphs.defaults["com.mekkablue.ShowGlyphFocus.showWhileMetrics"] = self.showWhileMetrics
			Glyphs.defaults["com.mekkablue.ShowGlyphFocus.showTriangle"] = self.showTriangle
			return True
		except:
			import traceback
			print(traceback.format_exc())
			return False

	def LoadPreferences( self ):
		Glyphs.registerDefault( "com.mekkablue.ShowGlyphFocus.color", (0.0, 0.0, 1, 0.1) )
		Glyphs.registerDefault( "com.mekkablue.ShowGlyphFocus.colorDarkMode", (0.9, 0.9, 0.9, 0.9) )
		Glyphs.registerDefault( "com.mekkablue.ShowGlyphFocus.showWhileMetrics", False )
		Glyphs.registerDefault( "com.mekkablue.ShowGlyphFocus.showRSB", True )
		Glyphs.registerDefault( "com.mekkablue.ShowGlyphFocus.showHighlight", True )
		Glyphs.registerDefault( "com.mekkablue.ShowGlyphFocus.showTriangle", True )
		

		self.color = Glyphs.defaults["com.mekkablue.ShowGlyphFocus.color"]
		self.showHighlight = Glyphs.defaults["com.mekkablue.ShowGlyphFocus.showHighlight"]
		self.showRSB = Glyphs.defaults["com.mekkablue.ShowGlyphFocus.showRSB"]
		self.showWhileMetrics = Glyphs.defaults["com.mekkablue.ShowGlyphFocus.showWhileMetrics"]
		self.showTriangle = Glyphs.defaults["com.mekkablue.ShowGlyphFocus.showTriangle"]

		darkModeIsTurnedOn = NSUserDefaults.standardUserDefaults().stringForKey_('AppleInterfaceStyle') == "Dark"	

		if darkModeIsTurnedOn:
			colorDarkMode = Glyphs.defaults["com.mekkablue.ShowGlyphFocus.colorDarkMode"]
			self.color = colorDarkMode

	
	@objc.python_method
	def transform(self, shiftX=0.0, shiftY=0.0, rotate=0.0, skew=0.0, scale=1.0):
		myTransform = NSAffineTransform.transform()
		if rotate:
			myTransform.rotateByDegrees_(rotate)
		if scale != 1.0:
			myTransform.scaleBy_(scale)
		if not (shiftX == 0.0 and shiftY == 0.0):
			myTransform.translateXBy_yBy_(shiftX,shiftY)
		if skew:
			skewStruct = NSAffineTransformStruct()
			skewStruct.m11 = 1.0
			skewStruct.m22 = 1.0
			skewStruct.m21 = math.tan(math.radians(skew))
			skewTransform = NSAffineTransform.transform()
			skewTransform.setTransformStruct_(skewStruct)
			myTransform.appendTransform_(skewTransform)
		return myTransform

	@objc.python_method
	def drawLine(self, x1, y1, x2, y2, strokeWidth):
		try:
			path = NSBezierPath.bezierPath()
			path.moveToPoint_(NSPoint(x1, y1))
			path.lineToPoint_(NSPoint(x2, y2))
			path.setLineWidth_(strokeWidth)
			NSColor.separatorColor().colorWithAlphaComponent_(0.4).set()
			# NSColor.keyboardFocusIndicatorColor().set()
			# NSColor.redColor().set()
			path.stroke()
		except:
			import traceback
			print(traeback.format_exc())

	@objc.python_method
	def drawTriangle(self, x1, y1, x2, y2, x3, y3):
		path = NSBezierPath.bezierPath()
		path.moveToPoint_(NSPoint(x1, y1))
		path.lineToPoint_(NSPoint(x2, y2))
		path.lineToPoint_(NSPoint(x3, y3))
		path.closePath()
		NSColor.separatorColor().colorWithAlphaComponent_(0.4).set()
		# NSColor.systemRedColor().colorWithAlphaComponent_(0.4).set()
		# NSColor.keyboardFocusIndicatorColor().set()
		path.fill()
	
	@objc.python_method
	def italicShift(self, yPos, angle, xHeight):
		'''
		ITALIC OFFSET. TAKEN FROM MARK FROMBERG'S SMART PLUMBLINES
		'''
		offset = math.tan(math.radians(angle)) * xHeight/2
		shift = math.tan(math.radians(angle)) * yPos - offset
		return shift

	@objc.python_method
	def drawRSB(self, layer):
		if self.showRSB:
			angle = layer.italicAngle

			xHeight = layer.master.xHeight
			x1, y1 = layer.width, layer.ascender
			x2, y2 = x1, layer.descender
			
			# draw line:
			strokeWidth = 0.75 * self.getScale() ** -0.9
			self.drawLine( 
				x1 + self.italicShift(y1, angle, xHeight), y1 , 
				x2 + self.italicShift(y2, angle, xHeight), y2, 
				strokeWidth,
				)
			
		# triangle:
		if self.showTriangle:
			triangleSize = 6.0 / self.getScale()  ** 1
			self.drawTriangle(
				layer.width/2-triangleSize + self.italicShift(y1+triangleSize, angle, xHeight), y1+triangleSize,
				layer.width/2 + self.italicShift(y1, angle, xHeight), y1,
				layer.width/2+triangleSize + self.italicShift(y1+triangleSize, angle, xHeight), y1+triangleSize,
				)
			self.drawTriangle(
				x1/2-triangleSize + self.italicShift(y2-triangleSize, angle, xHeight), y2-triangleSize,
				x1/2 + self.italicShift(y2, angle, xHeight), (y2),
				x1/2+triangleSize + self.italicShift(y2-triangleSize, angle, xHeight), y2-triangleSize,
				)
	
	@objc.python_method
	def drawLSB(self, layer):
		if self.showRSB:
			angle = layer.italicAngle

			xHeight = layer.master.xHeight
			x1, y1 = 0, layer.ascender
			x2, y2 = x1, layer.descender
			
			# draw line:
			strokeWidth = 0.5 * self.getScale() ** -0.9
			self.drawLine( 
				x1 + self.italicShift(y1, angle, xHeight), y1 , 
				x2 + self.italicShift(y2, angle, xHeight), y2, 
				strokeWidth,
				)
		
		# triangle:
		if self.showTriangle:
			triangleSize = 6.0 / self.getScale()  ** 1
			self.drawTriangle(
				layer.width/2-triangleSize + self.italicShift(y2, angle, xHeight), y2,
				layer.width/2 + self.italicShift(y2+triangleSize, angle, xHeight), (y2+triangleSize),
				layer.width/2+triangleSize + self.italicShift(y2, angle, xHeight), y2,
				)
			self.drawTriangle(
				layer.width/2-triangleSize + self.italicShift(y1+triangleSize, angle, xHeight), y1+triangleSize,
				layer.width/2 + self.italicShift(y1, angle, xHeight), y1,
				layer.width/2+triangleSize + self.italicShift(y1+triangleSize, angle, xHeight), y1+triangleSize,
				)

	@objc.python_method
	def background(self, layer):
		if self.showWhileMetrics and not Glyphs.defaults["showMetrics"]: return 
		currentTab = layer.parent.parent.currentTab
		if self.conditionsAreMetForDrawing():
			italicAngle = layer.master.italicAngle
			skewOriginHeight = layer.master.xHeight/2
			shiftX = math.tan( math.radians(italicAngle) ) * skewOriginHeight * -1
			transform = self.transform(skew=italicAngle, shiftX=shiftX)
			if self.showHighlight:
				NSColor.colorWithRed_green_blue_alpha_(*self.color).set()
				focusRect = NSRect( 
					NSPoint(0.0,layer.master.descender),
					NSSize(layer.width,layer.master.ascender-layer.master.descender),
					)
				focusField = NSBezierPath.bezierPathWithRect_(focusRect)

				

				focusField.transformUsingAffineTransform_(transform)
				focusField.appendBezierPath_( layer.completeBezierPath.bezierPathByReversingPath() )
				focusField.fill()

			
			if currentTab.direction == 0 :
				self.drawRSB(layer)
			if currentTab.direction == 2 :
				self.drawLSB(layer)

	# @objc.python_method
	# def conditionalContextMenus(self):

	# 	# Empty list of context menu items
	# 	contextMenus = []

	# 	# Execute only if layers are actually selected
	# 	if Glyphs.font.selectedLayers:
	# 		layer = Glyphs.font.selectedLayers[0]
			
	# 		# Exactly one object is selected and it’s an anchor
	# 		if len(layer.selection) == 1 and type(layer.selection[0]) == GSAnchor:
					
	# 			# Add context menu item
	# 			contextMenus.append({"name": "Randomly move anchor", "action": self.randomlyMoveAnchor})

	# 	# Return list of context menu items
	# 	return contextMenus
		
