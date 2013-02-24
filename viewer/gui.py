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

import pygtk
import gtk
import gtk.glade
#import inspect
import pango
#import sys
#import os

class viewer:
	
	from library import icc
	profile = None
	
	def __init__(self, icc_file=None):
				
		#Set the Glade file
		self.gladefile = "viewer/gui/main.glade"  
		self.wTree = gtk.Builder()
		self.wTree.add_from_file(self.gladefile)
		
		self.window = self.wTree.get_object("main_window")
		self.file_chooser = self.wTree.get_object("filechooserbutton")
		self.frame = self.wTree.get_object("content_frame")
		self.frame_label = self.wTree.get_object("label_header")
		self.frame_content = self.wTree.get_object("content_alignment")
				
		#Create our dictionay and connect it
		dic = { "on_filechooserbutton_file_set" : self.open_file,
				"on_window_destroy" : gtk.main_quit,
				"on_tag_table_tree_button_press_event": self.row_selected,
				"on_tag_table_tree_key_press_event": self.row_selected,
				}
		self.wTree.connect_signals(dic)
		self.window.drag_dest_set(gtk.DEST_DEFAULT_HIGHLIGHT, [], 0)
		
		#self.xyz_graph = self.wTree.get_object("xyz_graph")
		#self.xyz_graph.connect("expose-event", self.graph_expose_cb)
		
		self.tree, self.tree_list = self.create_columns(self.wTree.get_object("tag_table_tree"))
		self.set_filefilter()
		
		self.row_active_id = self.tree.connect("row_activated", self.row_activated_cb)
		
		if icc_file: 
			self.open_file(icc_file=icc_file)
			self.file_chooser.select_filename(icc_file)
		else:
			child = gtk.Label("Please select an icc profile to inspect.")
			child.set_use_markup(True)
			self.replace_child(child)	
			self.frame_label.set_text("<b>Welcome</b>")
			self.frame_label.set_use_markup(True)
		
		self.window.show()
		
		if self.window:
			self.window.connect("destroy", gtk.main_quit)
	
		gtk.main()
	
	def row_selected(self, one, two):
		#print one, two
		return
	
	
	def replace_child(self, child=None):
		old = self.frame_content.get_children()
		
		if child is None:
			return False;
		else:
			if len(old) is not 0:
				self.frame_content.remove(old[0])

			if child.get_parent() is not None:
				child.reparent(self.frame_content)
			else:
				self.frame_content.add(child)

			child.show()
		

	def row_activated_cb(self, treeView=None, row_num=None, treeViewColumn=None):
		row = row_num[0]-1
		signature,offset,size = self.profile.tag_array()[row]
		
		if(row_num[0]==0):	
			from header_view import header_view
			header_view(self)
			
		elif(signature=='desc' or signature=='cprt'
		or signature=='chad' or signature=='lumi'):
			from label_view import label_view
			label_view(self,row)
			
		elif(signature[1:4]=='XYZ'):		
			from xyz_view import xyz_view
			xyz_view(self,row)
		
		elif(signature=='wtpt'):		
			from xyz_view import xyz_view
			xyz_view(self,row)
		
		elif(signature=='bkpt'):		
			from xyz_view import xyz_view
			xyz_view(self,row)
		
		elif(signature[1:4]=='TRC'):		
			from trc_view import trc_view
			trc_view(self,row)
			
		else:
			from hex_view import hex_view
			hex_view(self,row)

	
	def create_columns(self, tree):
		tree_list = gtk.ListStore(int,int,str,int,int)
		
		column = gtk.TreeViewColumn("#", gtk.CellRendererText(), text=1)
		column.set_expand(True)
		tree.append_column(column)
	
		column = gtk.TreeViewColumn("Signature", gtk.CellRendererText(), text=2)
		column.set_expand(True)
		tree.append_column(column)
		
		column = gtk.TreeViewColumn("Offset", gtk.CellRendererText(), text=3)
		column.set_expand(True)
		tree.append_column(column)
		
		column = gtk.TreeViewColumn("Size", gtk.CellRendererText(), text=4)
		column.set_expand(True)
		tree.append_column(column)
		return tree, tree_list
		
	def populate_tag_table(self):
		self.tree_list.clear()
		self.tree_list.append([0,0,"header", 0, 128])
		
		i=1
		for k in self.profile.tag_array():
			tag_name, begin, lenght = k
			self.tree_list.append([i,i,tag_name, int(begin), int(lenght)])
			i = i + 1

		self.tree.set_model(None)
		self.tree.set_model(self.tree_list)
	
	def set_filefilter(self):	
		#self.file_filter = self.wTree.get_object("file_filter_list")
		#self.file_filter.set_name("Icc Profile")
		#self.file_filter.add_pattern("*.icc")
		#self.file_chooser.add_filter(self.file_filter)
		return
		
	def open_file(self, widget=None, icc_file=None):		
		if(self.file_chooser.get_filename()):
			icc_file = self.file_chooser.get_filename()
		
		if icc_file.endswith('.icc'):
			try:		
				self.profile = self.icc.open_file(icc_file)
				self.populate_tag_table()
				self.row_activated_cb(None,(0,),None)
			except IOError:
				print "IOError"
		else:
			child = gtk.Label("Please select *.icc file.")
			child.set_use_markup(True)
			self.replace_child(child)
			self.frame_label.set_text("<b>Wrong file type!</b>")
			self.frame_label.set_use_markup(True)	
