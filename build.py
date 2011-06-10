#!/usr/bin/env python

# Parchment build script
#
# Copyright (c) 2008-2011 The Parchment Contributors
# BSD licenced
# http://code.google.com/p/parchment

# Lists of files to combine together
includes = (
	('.build/parchment.js', (
		'src/parchment/intro.js',
		'src/lib/class.js',
		'src/lib/iff.js',
		'src/plugins/remedial.js',
		'src/parchment/error-handling.js',
		'src/parchment/file.js',
		'src/parchment/ui.js',
		'src/parchment/library.js',
		'src/parchment/gnusto.js',
		'src/parchment/outro.js',
	)),
	('.build/zmachine.js', (
		'src/gnusto/runner/zui.js',
		'src/plugins/quetzal.js',
		'src/gnusto/runner/runner.js',
		'src/gnusto/runner/console.js',
	)),
	('.build/quixe.js', (
		'src/quixe/quixe/quixe.js',
		'src/quixe/quixe/gi_dispa.js',
	)),
	('.build/glkote.js', (
		'src/quixe/glkote/glkote.js',
		'src/quixe/glkote/dialog.js',
		'src/quixe/glkote/glkapi.js',
	)),
)

# List of files to compress (with debug code removed)
compress = (
	('src/gnusto/engine/gnusto-engine.js', 'Parchment/gnusto.min.js'),
	('.build/parchment.js', 'Parchment/parchment.min.js'),
	('.build/zmachine.js', 'Parchment/zmachine.min.js'),
)

import datetime
import os
import re

# Today's date
today = str(datetime.date.today())

# regex for debug lines, and manifest date replacement
debug = re.compile('(;;;.+$)|(/\* DEBUG \*/[\s\S]+?(/\* ELSEDEBUG|/\* ENDDEBUG \*/))', re.M)
manifest = re.compile('\[INTERPRETERVERSION\].+?\[\]?', re.S)

# Create .build directory if needed
if not os.path.isdir('.build'):
	os.makedirs('.build')

# Combine source files together to make 'packages'
for package in includes:
	print 'Building package: ' + package[0]
	output = open(package[0], 'w')
	for include in package[1]:
		data = file(include).read()
		output.write(data)
	output.close()
		
# Compress these files, requires the YUI Compressor. Icky Java
for package in compress:
	print 'Compressing file: ' + package[1]
	
	# Strip out debug lines beginning with ;;;
	data = file(package[0]).read()
	data = debug.sub('', data)
	
	# Set the date
	data = data.replace('BUILDDATE', today)
	
	# Write to a temp file
	output = open('.build/temp', 'w')
	output.write(data)
	output.close()
	
	# Compress!
	command = 'java -jar ../yuicompressor-2.4.2.jar --type js .build/temp -o %s' % package[1]
	os.system(command)

# Set the date in (manifest).txt too
print 'Updating (manifest).txt'
data = file('Parchment/(manifest).txt').read()
data = manifest.sub('[INTERPRETERVERSION]\nParchment for Inform 7 (' + today + ')\n[]', data)
output = open('Parchment/(manifest).txt', 'w')
output.write(data)
output.close()
