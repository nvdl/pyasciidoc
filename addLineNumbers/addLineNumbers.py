#!/usr/bin/python
# -*- coding: utf-8 -*-
#==================================================================================================
'''
This module adds line numbers to an asciidoc document.
Use a directive to invoke line numbering as in the following examples.

Examples:

Do not add line numbers at all (or comment out the line with "//")
:line-numbering:section,n:code,n

Add line numbers in sections
:line-numbering:section,y:code,n

Add line numbers in sections and code blocks
:line-numbering:section,y:code,y

Add line numbers in code blocks only
:line-numbering:section,n:code,y

Coded by nvd
Email: oo.nvd.oo@gmail.com

TODO: Use cStringIO to improve speed (if needed).
'''
#==================================================================================================
import sys
import os
from platform import system
#==================================================================================================
class LineNumbering():

	def __init__(self):
		pass
		
	def __del__(self):
		pass
#==================================================================================================
	def process(self, text, params):

		try:
			osystem = system()
		
			if osystem == "Linux":
				LF = "\n"
			elif osystem == "Windows":
				LF = "\r\n"
			else:
				LF = "\n"

			# Need a header reader for it (later)
			# :line-numbering:section,y:code,y
			if not (":line-numbering:section," in text):
				return text

			text = text.replace("\r", "")
			lines = text.split("\n")
			
			sectionNumbering = False
			codeNumbering = False
			
			for i in xrange(len(lines)):
				line = lines[i]

				if ":line-numbering:section," in line:
					if not line[:2] == "//": # If not commented out
						fields = line.split(":")
						sectionNumbering = fields[2].split(",")[1]
						codeNumbering = fields[3].split(",")[1]
					
						if sectionNumbering == "y":
							sectionNumbering = True
						else:
							sectionNumbering = False
					
						if codeNumbering == "y":
							codeNumbering = True
						else:
							codeNumbering = False
					
					del lines[i]
					break

			print "sectionNumbering:", sectionNumbering
			print "codeNumbering:", codeNumbering
			
			if sectionNumbering == False and codeNumbering == False:
				print "No line numbers to add"
				return text

			# Do not number lines starting with these entries (incomplete for a while)
			directives = ["[", "."]
			
			numberingFormat = params[0]
	
			sectionStarted = False
			skipEmptyLines = False
			codeBlockStarted = False
			lineNumber = 1
			
			retText = ""

			for line in lines:

				if line[:2] == "==" and sectionNumbering:
					sectionStarted = True
					skipEmptyLines = True
					lineNumber = 1
				
					toWrite = line
				
				elif line == "----":

					sectionStarted = False

					if codeNumbering:
						codeBlockStarted = not codeBlockStarted
						lineNumber = 1

						if codeBlockStarted:
							skipEmptyLines = False
						else:
							skipEmptyLines = True

					toWrite = line

				elif sectionStarted or codeBlockStarted:
					if line == "" and skipEmptyLines:
						toWrite = line
					elif line[:1] in directives:
						toWrite = line
					else:
						toWrite = format(lineNumber, numberingFormat) + ": " + line

						if sectionStarted and not codeBlockStarted:
							toWrite += " +"

						lineNumber += 1					

				else:
					toWrite = line
				
				retText += toWrite + LF
				
			return retText

		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			errorStr = "Type: " + str(exc_type) + "\n"
			errorStr += "Exception: " + str(exc_obj) + "\n"
			errorStr += "Line: " + str(exc_tb.tb_lineno) + "\n"
			sys.stderr.write(errorStr)
#==================================================================================================
if __name__ == "__main__":

	if len(sys.argv) < 3:
		print "Usage: thisScript [fileIn] [fileOut]"
		sys.exit(-1)

	fNameIn = sys.argv[1]
	fNameOut = sys.argv[2]

	if not os.path.isfile(fNameIn):
		print '"' + fName + '"' + " does not exist"
		sys.exit(-1)

	with open(fNameIn, "r") as f:
		text = f.read()
		
	lineFormat = "03" # Add leading 0s to line numbers if needed
	
	lineNumbering = LineNumbering()
	retText = lineNumbering.process(text, (lineFormat,))
	
	with open(fNameOut, "w") as f:
		f.write(retText)
		f.flush()

	print "Done"
#==================================================================================================
