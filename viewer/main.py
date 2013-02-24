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

def main(argv=None):
	__process_argvs(argv)
	
	
def __process_argvs(argv=None):
	options = [option for option in argv if option.startswith("-")]
	arguments = [argument.strip() for argument in argv if not argument.startswith("-")]
		
	if len(options) > 1 or len(arguments) > 2: __quit_error()
		
	if len(options) and len(arguments):
		if options[0] in ('-c','--console'): __open_in_cmd(arguments[1])
	elif len(arguments) == 2: __open_in_gui(arguments[1])
	else: __open_in_gui()


def __open_in_cmd(icc_file=None):
	if icc_file.endswith(".icc"):
		from viewer import cmd
		cmd.open_icc(icc_file)
	else: __quit_error()


def __open_in_gui(icc_file=None):
	from viewer import gui
	if icc_file != None and icc_file.endswith(".icc"):
		gui.viewer(icc_file)
	else:
		gui.viewer(False)


def __quit_error():
	import sys
	print "Start Icc Viewer:"
	print "\tpyicc.py"
	print "Open icc file in gui:"
	print "\tpyicc.py /path/to/icc/file.icc"
	print "Print icc file content in command line:"
	print "\tpyicc.py -c /path/to/icc/file.icc"
	sys.exit()
