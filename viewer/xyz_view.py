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

class xyz_view:
	
	def __init__(self, parent, row):
		self.parent = parent
		self.xyz_graph = parent.wTree.get_object("xyz_graph")
		self.graph_expose_id = self.xyz_graph.connect("expose-event", self.graph_expose_cb)
		
		self.tree = self.parent.wTree.get_object("tag_table_tree")
		self.row_active_id = self.tree.connect("row_activated", self.cleanup)
		
		# get the tree selection
		selection = self.parent.tree.get_selection()
		
		#from tree selection get treemodel and treeiter
		treemodel, treeiter = selection.get_selected()
		signature = treemodel.get_value(treeiter,2)
		
		if signature == 'rXYZ':
			self.parent.frame_label.set_text("<b>Red Colorant Tag</b>")
		elif signature == 'gXYZ':
			self.parent.frame_label.set_text("<b>Green Colorant Tag</b>")
		elif signature == 'bXYZ':
			self.parent.frame_label.set_text("<b>Blue Colorant Tag</b>")
		elif signature == 'wtpt':
			self.parent.frame_label.set_text("<b>MediaWhitePoint Tag</b>")
		elif signature == 'bkpt':
			self.parent.frame_label.set_text("<b>MediaBlackPoint Tag</b>")
			
		self.parent.frame_label.set_use_markup(True)
		
		self.show_xyz(self.parent.profile.tag_array_data()[row])
		
	def cleanup(self, treeView=None, row_num=None, treeViewColumn=None):
		self.xyz_graph.disconnect(self.graph_expose_id)
		self.tree.disconnect(self.row_active_id)
		
	def show_xyz(self, data=None):
				
		child = self.parent.wTree.get_object("xyzview")
		
		X,Y,Z = self.parent.profile.xyz_number(data)
		
		entry_X = self.parent.wTree.get_object("entry_X")
		entry_Y = self.parent.wTree.get_object("entry_Y")
		entry_Z = self.parent.wTree.get_object("entry_Z")
		self.entry_x = self.parent.wTree.get_object("entry_x")
		self.entry_y = self.parent.wTree.get_object("entry_y")
		
		entry_X.set_text("%.5f" % X)
		entry_Y.set_text("%.5f" % Y)
		entry_Z.set_text("%.5f" % Z)
		self.entry_x.set_text("%.6f" % (X/(X+Y+Z)))
		self.entry_y.set_text("%.6f" % (Y/(X+Y+Z)))

		self.parent.replace_child(child)
		
	def graph_expose_cb(self, graph, event):
		global gc

		#gc = area.get_style().fg_gc[gtk.STATE_NORMAL]
		gc = graph.get_window().new_gc()
		colormap = graph.get_colormap()
	
		#print graph.window.get_size()
		#graph window size (x=448,y=424)

		light_gray = colormap.alloc_color(50000, 50000, 50000)
		gray = colormap.alloc_color(30000, 30000, 30000)
		black = colormap.alloc_color(0, 0, 0)
		white = colormap.alloc_color(65535, 65535, 65535)
	
		origin_x = 24
		origin_y = 400
	
		# axis
		pangolayout = graph.create_pango_layout("y")
		pangolayout.set_markup("<b>y</b>")
		font = pango.FontDescription("sans 12")
		pangolayout.set_font_description(font)
		graph.window.draw_layout(gc, 10,0, pangolayout,black)
	
		pangolayout = graph.create_pango_layout("x")
		pangolayout.set_markup("<b>x</b>")
		font = pango.FontDescription("sans 12")
		pangolayout.set_font_description(font)
		graph.window.draw_layout(gc, 435,402, pangolayout,black)		
	
		pixbuf = gtk.gdk.pixbuf_new_from_file("viewer/ciexyz.png")
		graph.window.draw_pixbuf(gc,pixbuf, 0, 0, origin_x, origin_y-360, -1, -1, gtk.gdk.RGB_DITHER_NORMAL, 0, 0)
	
		gc.line_width = 1
		gc.foreground = light_gray
		r_x = int(round(origin_x + (0.64 * 400),0))
		r_y = int(round(origin_y - (0.33 * 400),0))
	
		g_x = int(round(origin_x + (0.30 * 400),0))
		g_y = int(round(origin_y - (0.60 * 400),0))
	
		b_x = int(round(origin_x + (0.16 * 400),0))
		b_y = int(round(origin_y - (0.06 * 400),0))
	
		graph.window.draw_line(gc,g_x,g_y,r_x,r_y)
		graph.window.draw_line(gc,g_x,g_y,b_x,b_y)
		graph.window.draw_line(gc,b_x,b_y,r_x,r_y)
	
		gc.foreground = gray
		for i in range(40,400, 40):
			graph.window.draw_line(gc,origin_x,origin_y-i,430,origin_y-i)
		
			number = (i/40.0)/10.0
			pangolayout = graph.create_pango_layout(str(number))
			graph.window.draw_layout(gc, origin_x-24,origin_y-i-7, pangolayout,black)
		
		for i in range(40,400, 40):
			graph.window.draw_line(gc,origin_x+i,origin_y,origin_x+i,0)
		
			number = (i/40.0)/10.0
			pangolayout = graph.create_pango_layout(str(number))
			graph.window.draw_layout(gc, origin_x+i-10,origin_y+7, pangolayout,black)
	
	
	
		gc.foreground = gray
		graph.window.draw_line(gc,24,0,24,448)
		graph.window.draw_line(gc,0,400,448,400)
	
		x = round(eval(self.entry_x.get_text()),2)
		y = round(eval(self.entry_y.get_text()),2)
		print x,y
		x = origin_x + (x * 10 * 40)
		y = origin_y - (y * 400)
		print x - origin_x,origin_y - y
		gc.line_width = 2
	
		# x-5 because the circle is 10 pixels wide. The center is therefore 5 pixels off
		# the same goes for y
		# graph.window.draw_arc(gc, True, origin_x-5, origin_y-5, 10, 10, 0, 360*64)
	
		gc.foreground = black
		graph.window.draw_arc(gc, False, int(round(x,0))-5, int(round(y,0))-5, 10, 10, 0, 360*64)
	
		pangolayout = graph.create_pango_layout("")
		pangolayout.set_markup("The gray triangle is the sRGB gamut")
		graph.window.draw_layout(gc, 125,10, pangolayout,black,light_gray)
