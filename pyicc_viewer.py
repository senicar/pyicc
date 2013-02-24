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
   
import sys
import os

try:
	import pygtk
	pygtk.require("2.0")
	import gtk
	import gtk.glade
except:
	print "You need to install pyGTK or GTKv2",
	sys.exit(1)
		
if __name__ == "__main__":
	from viewer.main import *
	sys.path.insert(0, os.getcwd())
	main(sys.argv)
