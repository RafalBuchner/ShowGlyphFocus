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
from Foundation import NSPoint, NSAffineTransform, NSAffineTransformStruct, NSRect
import math


	


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

	@objc.python_method
	def LoadPreferences( self ):
		Glyphs.registerDefault( "com.mekkablue.ShowGlyphFocus.color", (0.5, 0.5, 0.5, 0.2) )
		Glyphs.registerDefault( "com.mekkablue.ShowGlyphFocus.colorDarkMode", (0.9, 0.9, 0.9, 0.9) )

		self.color = Glyphs.defaults["com.mekkablue.ShowGlyphFocus.color"]

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
	def background(self, layer):
		NSColor.colorWithRed_green_blue_alpha_(*self.color).set()
		focusRect = NSRect( 
			NSPoint(0.0,layer.master.descender),
			NSSize(layer.width,layer.master.ascender-layer.master.descender),
			)
		focusField = NSBezierPath.bezierPathWithRect_(focusRect)

		italicAngle = layer.master.italicAngle
		skewOriginHeight = layer.master.xHeight/2
		shiftX = math.tan( math.radians(italicAngle) ) * skewOriginHeight * -1
		transform = self.transform(skew=italicAngle, shiftX=shiftX)

		focusField.transformUsingAffineTransform_(transform)
		focusField.appendBezierPath_( layer.completeBezierPath.bezierPathByReversingPath() )
		focusField.fill()
		
