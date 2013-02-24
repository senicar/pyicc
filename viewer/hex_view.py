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

class hex_view:
	
	def __init__(self,parent,row):
		self.parent = parent		
		self.show_hexview(self.parent.profile.tag_array_data()[row])
		
		self.parent.frame_label.set_text("<b>Private or unkown tag</b>")
		self.parent.frame_label.set_use_markup(True)
	
	def show_hexview(self, data=None):
		
		child = self.parent.wTree.get_object("hexview")
		hex_text = self.parent.wTree.get_object("hex_text")
		hex_buffer = self.parent.wTree.get_object("hex_buffer")		
		
		data_text = list(data)

		bytes_in_line = 12
		
		extra_chars = 0
		while (len(data_text)) % (bytes_in_line):
			data_text.append('\x00')
			extra_chars = extra_chars + 1
			
		text = ''		
		#all bytes
		i=0
		#number of rows
		y=0
		
		while i < len(data_text):
			line = ''
			line_text = ''
						
			x=0
			while x < (bytes_in_line):
				line = line + data_text[i+x].encode('hex') + ' '
				x=x+1
				
			x=0
			while x < (bytes_in_line):
				line_text = line_text + data_text[i+x] + ''
				x=x+1
			line_text = line_text.replace('\x00','.')
			line_text = line_text.replace('\n','.')
			line_text = line_text.replace('\r','.')
			line_text = line_text.replace('\t','.')
			
			line_num_hex = list(hex(y*bytes_in_line))[2:]
			line_num_hex.reverse()
			while (len(line_num_hex)) % 8:
				line_num_hex.append('0')
			line_num_hex.reverse()
			
			try:
				line_text = line_text.decode('ascii','replace')
			except UnicodeDecodeError:
				print "error"
			else:
				line_text = line_text.decode('ascii','replace')
			
			text = text + ''.join(line_num_hex) + ' | ' + line
			text = text + '| ' + line_text + '\n'
			y=y+1
			i = i + bytes_in_line
				
		hex_buffer.set_text(text[0:-(extra_chars + 1)]);
		#line_num_buffer.set_text(text[:-2]);
		font = pango.FontDescription("monospace")
		hex_text.modify_font(font)
		
		self.parent.replace_child(child)
