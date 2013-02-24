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


import mmap
import struct

class icc:

	data = False
	
	####################################################################
	#
	# ICC Tags, Hex codes, Signatures
	#
	####################################################################
	
	# Required ICC tags
	# -----------------------------
	
	# Profil/Device Class signature
	# -----------------------------
	
	profiles = {}
	profiles['\x73\x63\x6E\x72'] = 'scnr' #'input_device' # 'scnr'
	profiles['\x6D\x6E\x74\x72'] = 'mntr' #'display_device' # 'mntr'
	profiles['\x70\x72\x74\x72'] = 'prtr' #'output_device' # 'prtr'
	profiles['\x6C\x69\x6E\x6B'] = 'link' #'device_link' # 'link'
	profiles['\x73\x70\x61\x63'] = 'spac' #'color_space_conversion' # 'spac'
	profiles['\x61\x62\x73\x74'] = 'abst' #'abstract' # 'abst'
	profiles['\x6E\x6D\x63\x6C'] = 'nmcl' #'named_color' # 'nmcl'
	
	
	# Color Space signature
	# -----------------------------
	
	color_spaces = {}
	color_spaces['\x58\x59\x5A\x20'] = 'XYZ ' # XYZData
	color_spaces['\x43\x4D\x59\x4B'] = 'CMYK' # cmykData
	color_spaces['\x11\x11\x42\x66'] = 'RGB ' # rgbData
	color_spaces['\x4C\x61\x00\xBB'] = 'Lab ' # labData
	color_spaces['\x4C\x75\x76\x20'] = 'Luv ' # luvData
	color_spaces['\x59\x43\x62\x72'] = 'YCbr' # YCbCrData
	color_spaces['\x59\x78\x79\x20'] = 'Yxy ' # YxyData
	color_spaces['\x52\x47\x42\x20'] = 'RGB ' # rgbData
	color_spaces['\x47\x52\x41\x59'] = 'GRAY' # grayData
	color_spaces['\x48\x53\x56\x20'] = 'HSV ' # hsvData
	color_spaces['\x48\x4C\x53\x20'] = 'HLS ' # hlsData
	color_spaces['\x43\x4D\x59\x4B'] = 'CMYK' # cmykData
	color_spaces['\x43\x4D\x59\x20'] = 'CMY ' # cmyData
	color_spaces['\x32\x43\x4C\x52'] = '2CLR' # 2colorData
	color_spaces['\x33\x43\x4C\x52'] = '3CLR' # 3colorData (if not listed above)
	color_spaces['\x34\x43\x4C\x52'] = '4CLR' # 4colorData (if not listed above)
	color_spaces['\x35\x43\x4C\x52'] = '5CLR' # 5colorData
	color_spaces['\x36\x43\x4C\x52'] = '6CLR' # 6colorData
	color_spaces['\x37\x43\x4C\x52'] = '7CLR' # 7colorData
	color_spaces['\x38\x43\x4C\x52'] = '8CLR' # 8colorData
	color_spaces['\x39\x43\x4C\x52'] = '9CLR' # 9colorData
	color_spaces['\x41\x43\x4C\x52'] = 'ACLR' # 10colorData
	color_spaces['\x42\x43\x4C\x52'] = 'BCLR' # 11colorData
	color_spaces['\x43\x43\x4C\x52'] = 'CCLR' # 12colorData
	color_spaces['\x44\x43\x4C\x52'] = 'DCLR' # 13colorData
	color_spaces['\x45\x43\x4C\x52'] = 'ECLR' # 14colorData
	color_spaces['\x46\x43\x4C\x52'] = 'FCLR' # 15colorData
	
	# Profile connection space (PCS)
	# -----------------------------
	
	profile_connection_spaces = {}
	profile_connection_spaces['\x58\x59\x5A\x20'] = 'XYZ' # XYZData
	profile_connection_spaces['\x4C\x61\x62\x20'] = 'Lab' # labData
	
	# Primary platform signatures
	# -----------------------------
	
	primary_platform_signatures = {}
	primary_platform_signatures['\x41\x50\x50\x4C'] = 'APPL' # Apple Computer, Inc.
	primary_platform_signatures['\x4D\x53\x46\x54'] = 'MSFT' # Microsoft Corporation
	primary_platform_signatures['\x53\x47\x49\x20'] = 'SGI' # Silicon Graphics, Inc.
	primary_platform_signatures['\x53\x55\x4E\x57'] = 'SUNW' # Sun Microsystems, Inc.
	primary_platform_signatures['\x54\x47\x4E\x54'] = 'TGNT' # Taligent, Inc.
	
	profileDescriptionTag = '\x64\x65\x73\x63' # desc
	
	redTRCTag = '\x72\x54\x52\x43' # rTRC
	
	redMatrixColumnTag = '\x72\x58\x59\x5A'
	
		
	XYZ = {'red':{},'green':{},'blue':{}}
	
	####################################################################
	#
	# __init__
	#
	####################################################################
	
	def __init__(self):
		return
	
	####################################################################
	#
	# ICC Header Information / Description
	#
	####################################################################
	
	def size(self):
		self.data.seek(0,0)
		return struct.unpack('>i',self.data.read(4))[0]
	
	def cmm_type(self):
		self.data.seek(4,0)
		return self.data.read(4).encode()
	
	def version(self):
		self.data.seek(8,0)
		#return struct.unpack('bbbb',self.data.read(4))
		return '0x' + self.data.read(4).encode('hex')[1:]
	
	def profile_device_class_sig(self):
		self.data.seek(12,0)
		hexdata = self.data.read(4)		
				
		if self.profiles.has_key(hexdata):
			return self.profiles[hexdata]
		else:
			return False
	
	def color_space(self):
		self.data.seek(16,0)
		hexdata = self.data.read(4)		
				
		if self.color_spaces.has_key(hexdata):
			return self.color_spaces[hexdata]
		else:
			return False
		
	def profile_connection_space(self):
		self.data.seek(20,0)
		hexdata = self.data.read(4)		
				
		if self.profile_connection_spaces.has_key(hexdata):
			return self.profile_connection_spaces[hexdata]
		else:
			return False
	
	def creation_datetime(self):
		self.data.seek(24,0)
		return struct.unpack('>hhhhhh',self.data.read(12))
	
	def file_signature(self):
		self.data.seek(36,0)
		return self.data.read(4)
	
	def primary_platform_signature(self):
		self.data.seek(40,0)
		hexdata = self.data.read(4)		
				
		if self.primary_platform_signatures.has_key(hexdata):
			return self.primary_platform_signatures[hexdata]
		else:
			return False
	
	def cmm_flags(self):
		
		# first bit for embedded profile 
		# (0 if not embedded, 1 if embedded in file)
		#
		# second bit, profile cannot be used independently from 
		# the embedded color data (1=True, 0=False)
		#
		# The least-significant 16 bits are reserved for the ICC
		
		self.data.seek(44,0)
		return struct.unpack('>bbbb',self.data.read(4))

	def device_manufacture(self):
		self.data.seek(48,0)
		return self.data.read(4).encode()

	def device_model(self):
		self.data.seek(52,0)
		return self.data.read(4).encode('hex')

	def device_attributes(self):
		
		# first bit, Reflective (0) or Transparency (1)
		# second bit, Glossy (0) or Matte (1)
		# third bit, Media polarity - Positive (0) or Negative (1)
		# fourth bit, Colour media (0), Black & white media (1)
		
		self.data.seek(56,0)
		return struct.unpack('>bbbb',self.data.read(4))
	
	def rendering_intent(self):
		
		# 0 = perceptual
		# 1 = relative colorimetric
		# 2 = saturation
		# 3 = absolute colorimetric
		
		self.data.seek(64,0)
		return struct.unpack('>i',self.data.read(4))[0]
	
	def illuminant(self):		
		self.data.seek(68,0)
		return self.xyz_number(self.data.read(12))
	
	def profile_creator_signature(self):
		self.data.seek(80,0)
		return self.data.read(4).encode()
	
	def profile_id(self):
		self.data.seek(84,0)
		return self.data.read(16).encode('hex')
	
	def reserved_bytes(self):
		self.data.seek(100,0)
		return self.data.read(28).encode('hex')
	
	####################################################################
	#
	# Tag table, tagged element data
	#
	####################################################################
	
	def tag_count(self):
		self.data.seek(128,0)
		return struct.unpack('>i',self.data.read(4))[0]
	
	def tag_get_by_key(self, key):
		"""Tag key number is the position key in the tag_array"""
		
		# 12 bytes for each tag		
		# tag table starts at 132 bytes
		tag_position = 132 + (12 * key)
		
		self.data.seek(tag_position,0)
		
		return (self.data.read(4).encode(), 
				struct.unpack('>i',self.data.read(4))[0], 
				struct.unpack('>i',self.data.read(4))[0])
	
	def tag_array(self):			
		"""Returns a list of tuples with signature,offset,size values"""
		tag_array = []
				
		for i in range(self.tag_count()):
			tag_array.append(self.tag_get_by_key(i))
				
		return tag_array
	
	def tag_array_data(self):
		
		data = []
		for i in self.tag_array():
			self.data.seek(i[1])
			data.append(self.data.read(i[2]))
		
		return data
	
	####################################################################
	#
	# Functions
	#
	####################################################################
	
	def xyz_number(self, xyz_bytes):
		if len(xyz_bytes) > 12:
			xyz_bytes_num = xyz_bytes[8:]
		else:
			xyz_bytes_num = xyz_bytes
			
		X,Y,Z = struct.unpack('>iii',xyz_bytes_num)
		X = (X / 65536.0)
		Y = (Y / 65536.0)
		Z = (Z / 65536.0)
		
		return X,Y,Z

	def curv(self, curv_data):
		curv_data = curv_data[4:]
		reserved, rows = struct.unpack('>ii',curv_data[:8])
		
		data = []
		
		if rows is 1:
			start = 8
			end = 10
			data.append(self.u8Fixed8Number(curv_data[start:end]))
		else:
			for i in range(rows):
				start = 8 + i*2
				end = 10 + i*2
				data.append(self.uInt16Number(curv_data[start:end]))
		
		return data

	def s15Fixed16ArrayType(self, sf32_data):
		sf32_numbers = sf32_data[8:]
		X,Y,Z, X1,Y1,Z1, X2,Y2,Z2 = struct.unpack('>iiiiiiiii',sf32_numbers)
		X = (X / 65536.0)
		Y = (Y / 65536.0)
		Z = (Z / 65536.0)
		
		X1 = (X1 / 65536.0)
		Y1 = (Y1 / 65536.0)
		Z1 = (Z1 / 65536.0)
		
		X2 = (X2 / 65536.0)
		Y2 = (Y2 / 65536.0)
		Z2 = (Z2 / 65536.0)
		
		return X,Y,Z, X1,Y1,Z1, X2,Y2,Z2
	
	def textType(self, text):
		return text[8:]
	
	def textDescriptionType(self, desc):
		#print struct.unpack('>i',desc[4:8])
		n = struct.unpack('>i',desc[8:12])[0]
		ascii_desc = desc[12:(12+n-1)]
		#print struct.unpack('>i',desc[n:n+4])
		
		# localized description count
		#m = struct.unpack('>i',desc[n+4:n+8])[0]
		#print m
		#print desc[n+23:m-1]
		#print desc[n:].encode('hex')
		#print struct.unpack('>h',desc[m:m+2])
		return ascii_desc
	
	def u8Fixed8Number(self, number):
		return struct.unpack('>h',number)[0] / 256.0
		
	def uInt16Number(self, number):
		return struct.unpack('>H',number)[0]
	
class open_file(icc):
	
	def __init__(self,icc_file):
		self.data = open(icc_file,'r+b')
