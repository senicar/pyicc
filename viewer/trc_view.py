#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 senicar
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pango
#import pygtk
import gtk

class trc_view:
	
	def __init__(self,parent,row):
		self.parent = parent
		self.row = row
		
		self.trc_draw_v = self.parent.wTree.get_object("trc_draw_v")
		self.trc_draw_v_expose_id = self.trc_draw_v.connect("expose-event", self.axisy_expose_cb)
			
		self.trc_draw_h = self.parent.wTree.get_object("trc_draw_h")
		self.trc_draw_h_expose_id = self.trc_draw_h.connect("expose-event", self.axisx_expose_cb)
		
		self.tree = self.parent.wTree.get_object("tag_table_tree")
		self.row_active_id = self.tree.connect("row_activated", self.cleanup)
		
		# get the tree selection
		selection = self.parent.tree.get_selection()
		
		#from tree selection get treemodel and treeiter
		treemodel, treeiter = selection.get_selected()
		signature = treemodel.get_value(treeiter,2)
		
		if signature == 'rTRC':
			self.parent.frame_label.set_text("<b>Red Curve Tag</b>")
		elif signature == 'gTRC':
			self.parent.frame_label.set_text("<b>Green Curve Tag</b>")
		elif signature == 'bTRC':
			self.parent.frame_label.set_text("<b>Blue Curve Tag</b>")
			
		self.parent.frame_label.set_use_markup(True)
		
		self.show_trc(self.parent.profile.tag_array_data()[self.row])
	
	def cleanup(self, treeView=None, row_num=None, treeViewColumn=None):
		self.trc_draw_h.disconnect(self.trc_draw_h_expose_id)
		self.trc_draw_v.disconnect(self.trc_draw_v_expose_id)
		self.tree.disconnect(self.row_active_id)
		
	def show_trc(self, data=None):
		child = self.parent.wTree.get_object("trc_view")				
		trc_curve = self.parent.wTree.get_object("trc_curve")
		trc_curve.realize()
		trc_curve.show()
		trc_curve.reset()
		label_gamma = self.parent.wTree.get_object("label_gamma")
		entry_gamma = self.parent.wTree.get_object("entry_gamma")
		
		gamma = self.parent.profile.curv(data)

		if len(gamma) > 1:
			entry_gamma.hide()
			label_gamma.set_text("%s points" % len(gamma))
			trc_curve.set_vector(gamma)
		else:
			entry_gamma.show()
			entry_gamma.set_text('%.5f' % gamma[0])
			label_gamma.set_text("Gamma:")
			trc_curve.set_gamma(gamma[0]**(-1))

		self.parent.replace_child(child)
	
	def axisy_expose_cb(self, graph, event):
		global gc

		#gc = area.get_style().fg_gc[gtk.STATE_NORMAL]
		gc = graph.get_window().new_gc()
		colormap = graph.get_colormap()
		black = colormap.alloc_color(0, 0, 0)
		
		font = pango.FontDescription("sans 8")
		# axis
		pangolayout = graph.create_pango_layout("65535")
		pangolayout.set_font_description(font)
		graph.window.draw_layout(gc, 0,0, pangolayout,black)
		
		pangolayout = graph.create_pango_layout("49149")
		pangolayout.set_font_description(font)
		graph.window.draw_layout(gc, 0,94, pangolayout,black)
		
		pangolayout = graph.create_pango_layout("32766")
		pangolayout.set_font_description(font)
		graph.window.draw_layout(gc, 0,191, pangolayout,black)
		
		pangolayout = graph.create_pango_layout("16383")
		pangolayout.set_font_description(font)
		graph.window.draw_layout(gc, 0,288, pangolayout,black)
		
		pangolayout = graph.create_pango_layout("0")
		pangolayout.set_font_description(font)
		graph.window.draw_layout(gc, 24,382, pangolayout,black)
	
	def axisx_expose_cb(self, graph, event):
		global gc

		#gc = area.get_style().fg_gc[gtk.STATE_NORMAL]
		gc = graph.get_window().new_gc()
		colormap = graph.get_colormap()
		black = colormap.alloc_color(0, 0, 0)
		
		font = pango.FontDescription("sans 8")
		# axis
		pangolayout = graph.create_pango_layout("65535")
		pangolayout.set_font_description(font)
		graph.window.draw_layout(gc, 415,0, pangolayout,black)
		
		pangolayout = graph.create_pango_layout("49149")
		pangolayout.set_font_description(font)
		graph.window.draw_layout(gc, 325,0, pangolayout,black)
		
		pangolayout = graph.create_pango_layout("32766")
		pangolayout.set_font_description(font)
		graph.window.draw_layout(gc, 222,0, pangolayout,black)
		
		pangolayout = graph.create_pango_layout("16383")
		pangolayout.set_font_description(font)
		graph.window.draw_layout(gc, 118,0, pangolayout,black)
		
		pangolayout = graph.create_pango_layout("0")
		pangolayout.set_font_description(font)
		graph.window.draw_layout(gc, 32,0, pangolayout,black)
