# encoding: utf-8

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

class ShowGlyphFocus(ReporterPlugin):

	def settings(self):
		self.menuName = Glyphs.localize({
			'en': u'Glyph Focus', 
			'de': u'Fokus auf aktuelle Glyphe',
		})
		
	def background(self, layer):
		#rectSize = 10000/self.getScale()	
		#grayRect  = NSRect( NSPoint(-rectSize,-rectSize), NSSize(rectSize*2+layer.width,2*rectSize) )
		#NSBezierPath.fillRect_(grayRect)

		NSColor.colorWithRed_green_blue_alpha_(0, 0, 0, 0.07).set()
		grayRect = NSRect( 
			NSPoint(0.0,layer.master.descender),
			NSSize(layer.width,layer.master.ascender-layer.master.descender),
			)
		focusField = NSBezierPath.bezierPathWithRect_(grayRect)
		focusField.appendBezierPath_( layer.completeBezierPath.bezierPathByReversingPath() )
		focusField.fill()
		
		
