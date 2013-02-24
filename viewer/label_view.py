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

class label_view:
	
	def __init__(self,parent,row):
		self.parent = parent
		self.row = row
		
		# get the tree selection
		selection = self.parent.tree.get_selection()
		
		#from tree selection get treemodel and treeiter
		treemodel, treeiter = selection.get_selected()
		signature = treemodel.get_value(treeiter,2)
		
		try:
			getattr(self, signature)()
		except AttributeError:
			print("No such function! Signature not supported")
	
	def desc(self,data=None):
		text = self.parent.profile.textDescriptionType(self.parent.profile.tag_array_data()[self.row])
		child = gtk.Label(text)
		child.set_use_markup(True)
		child.set_line_wrap(True)
		self.parent.replace_child(child)
		self.parent.frame_label.set_text("<b>Description</b>")
		self.parent.frame_label.set_use_markup(True)
	
	def chad(self, data=None):
		self.parent.frame_label.set_text("<b>Chromatic Adaptation Tag</b>")
		self.parent.frame_label.set_use_markup(True)
		
		data = self.parent.profile.tag_array_data()[self.row]
		numbers = self.parent.profile.s15Fixed16ArrayType(data)
		
		text = '%.6f\t%.6f\t%.6f\n%.6f\t%.6f\t%.6f\n%.6f\t%.6f\t%.6f' % numbers
		child = gtk.Label(text)
		child.set_use_markup(True)
		self.parent.replace_child(child)
	
	def lumi(self, data=None):
		self.parent.frame_label.set_text("<b>Luminance Tag</b>")
		self.parent.frame_label.set_use_markup(True)
		
		data = self.parent.profile.tag_array_data()[self.row]
		text = '%.6f candelas per square meter' % self.parent.profile.xyz_number(data)[1]
		child = gtk.Label(text)
		child.set_use_markup(True)
		self.parent.replace_child(child)
	
	def cprt(self, data=None):
		text = self.parent.profile.textType(self.parent.profile.tag_array_data()[self.row])
		child = gtk.Label(text)
		child.set_use_markup(True)
		child.set_line_wrap(True)
		self.parent.replace_child(child)
		self.parent.frame_label.set_text("<b>Copyright</b>")
		self.parent.frame_label.set_use_markup(True)
