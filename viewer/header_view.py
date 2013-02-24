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

class header_view:
	
	def __init__(self,parent):
		self.parent = parent
		self.show_header_info()
		
	def show_header_info(self):
		self.parent.frame_label.set_text("<b>Header Info</b>")
		self.parent.frame_label.set_use_markup(True)
				
		header_info_box = self.parent.wTree.get_object("header_info")
		
		size = self.parent.wTree.get_object("size")
		size.set_text(str(self.parent.profile.size()) + " bytes")
		
		cmm = self.parent.wTree.get_object("cmm")
		cmm.set_text(str(self.parent.profile.cmm_type()))
		
		version = self.parent.wTree.get_object("version")
		version.set_text(str(self.parent.profile.version()))
		
		device_class = self.parent.wTree.get_object("device_class")
		device = self.parent.profile.profile_device_class_sig()
		device_arr = {'scnr': 'Input Device',
					'mntr': 'Display Device',
					'prtr': 'Output Device',
					'link': 'Device Link',
					'spac': 'ColorSpace Conversion',
					'abst': 'Abstract',
					'nmcl': 'Named Colour'
					}
		
		device_class.set_text(str(device_arr[device]))
		
		color_space = self.parent.wTree.get_object("color_space")
		color_space.set_text(str(self.parent.profile.color_space()))
		
		pcs = self.parent.wTree.get_object("pcs")
		pcs.set_text(str(self.parent.profile.profile_connection_space()))
		
		date = self.parent.wTree.get_object("date")
		date_text = "%s/%s/%s, %s:%s:%s" % self.parent.profile.creation_datetime()
		date.set_text(str(date_text))
		
		magic = self.parent.wTree.get_object("magic")
		magic.set_text(str(self.parent.profile.file_signature()))
		
		platform = self.parent.wTree.get_object("platform")
		platform.set_text(str(self.parent.profile.primary_platform_signature()))
		
		flags = self.parent.wTree.get_object("flags")
		flag = self.parent.profile.cmm_flags()
		f0 = ('not embedded', 'embedded')
		f1 = ('independetly', 'cannot be used independetly')
		flag_text = "%s, %s" % (f0[flag[0]], f1[flag[1]])
		flags.set_text(str(flag_text))
		
		manufacture = self.parent.wTree.get_object("manufacture")
		if len(self.parent.profile.device_manufacture().replace('\00','')) > 0:		
			manufacture.set_text(str(self.parent.profile.device_manufacture()))
		
		device_model = self.parent.wTree.get_object("model")
		device_model.set_text(str(self.parent.profile.device_model()))
		
		attributes = self.parent.wTree.get_object("attribute")
		attr = self.parent.profile.device_attributes()
		f0 = ('Relfective', 'Transparency')
		f1 = ('Glossy', 'Matte')
		f2 = ('Positive','Negative')
		f3 = ('Color', 'Black & White')
		attr_text = "%s, %s, %s, %s" % (f0[attr[0]], f1[attr[1]], f2[attr[2]], f3[attr[3]])
		attributes.set_text(str(attr_text))
		
		intent = self.parent.wTree.get_object("intent")
		intent_arr = ('Perceptual', 'Media-Relative Colorimetric', 'Saturation', 'ICC-Absolute Colorimetric')
		intent.set_text(str(intent_arr[self.parent.profile.rendering_intent()]))
		
		illuminant = self.parent.wTree.get_object("illuminant")
		xyz = self.parent.profile.illuminant()
		xyz_text = "X=%.5f, Y=%.5f, Z=%.5f" % (xyz[0], xyz[1], xyz[2])
		illuminant.set_text(str(xyz_text))
		
		creator = self.parent.wTree.get_object("creator")
		creator.set_text(str(self.parent.profile.profile_creator_signature()))
		
		profile_id = self.parent.wTree.get_object("profile_id")
		profile_id.set_text(str(self.parent.profile.profile_id()))
				
		self.parent.replace_child(header_info_box)
