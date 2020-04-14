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

class ShowGlyphFocus(ReporterPlugin):

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'Glyph Focus', 
			'de': 'Fokus auf aktuelle Glyphe',
			'fr': 'focus sur le glyphe actuel',
			'es': 'concentración en el glifo actual',
		})
	
	@objc.python_method
	def background(self, layer):
		NSColor.colorWithRed_green_blue_alpha_(0.5, 0.5, 0.5, 0.2).set()
		grayRect = NSRect( 
			NSPoint(0.0,layer.master.descender),
			NSSize(layer.width,layer.master.ascender-layer.master.descender),
			)
		focusField = NSBezierPath.bezierPathWithRect_(grayRect)
		focusField.appendBezierPath_( layer.completeBezierPath.bezierPathByReversingPath() )
		focusField.fill()
		
