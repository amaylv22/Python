#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os.path
import time
import cherrypy

#CherryPy needs an absolute path when dealing with static data
_curdir = os.path.join(os.getcwd(), os.path.dirname(__file__))

#The notes will be keeped in a global list
#Please note that it is hazardous to use a simple list here, since we will run the application in a
#multi-threaded enviroment which will not protect the access to the list
#In a more realistic application we would need either to use a thread safe object or to manually protect from
#concurrent access to this list

_notes = []

#~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# HTML templates

_header = """
<html>
	<head>
		<title>Random notes</title>
		<link rel="stylesheet" type="text/css" href="/style.css"></link>
	</head>
	
	<body>
	<div class="container">"""

_footer = """
	</div>
	</body>
</html>"""

_note_form = """
	<div class="form">
	<form method="post" action="post" class="form">
		<input type="text" value="Your note here ..." name="text" size="60"></input>
		<input type="submit" value="Add"></input>
	</form>
	</div>"""

_author_form = """
	<div class="form">
	<form method="post" action="set">
		<input type="text" name="name"></input>
		<input type="submit" value="Switch"></input>
	</form>
	</div>"""

_note_view = """
	<br />
	<div>
		%s
		<div class="info">%s - %s <a href="/note/%d">(%d)</a></div>
	</div>"""

#~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# Our only domain object (sometimes referred as to a Model)

class Note(object):
	def __init__ (self, author, note):
		self.id = None
		self.author = author
		self.note = note
		self.timestamp = time.gmtime(time.time())
	
	def __str__ (self):
		return self.note

#~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# The main entry point of the Note Application

class NoteApp:
	"""The base application wich will be hosted by CherryPy"""
	
	#Here we tell CherryPy we will enable the session from this level of the tree of published objects as
	#well as its sub-levels
	_cp_config = { 'tools.sessions.on': True }
	
	def _render_note (self, note):
		"""Helper to render a note in HTML"""
		return _note_view % (note, note.author, time.strftime("%a, %d %b %Y %H:%M:%S", note.timestamp), note.id, note.id)
	
	@cherrypy.expose
	def index(self):
		#Retrieve the author stored in the current session (None if not defined)
		author = cherrypy.session.get('author', None)
		
		page = [_header]
		
		if author:
			page.append("""
			<div><span>Hello %s, please leve us a note. <a href="author">Switch identity</a>.</span></div>""" % (author))
			page.append(_note_form)
		else:
			page.append("""<div><span><a href="author">Set your identity</a></span></div>""")
		
		notes =_notes[:]
		notes.reverse()
		
		for note in notes:
			page.append(self._render_note(note))
		
		page.append(_footer)
		
		#returns to the cherrypy server the page to render
		return page
	
	@cherrypy.expose
	def note(self, id):
		#Retrieve the note attached to the given id
		try:
			note = _notes[int(id)]
		except:
			#If the ID was not valid, let's tell the client we did not find it
			raise cherrypy.NotFound
		
		return [_header, self._render_note(note), _footer]
	
	@cherrypy.expose
	def post(self, text):
		author = cherrypy.session.get('author', None)
		
		#Here if the author was not in the session we redirect the client to the author form
		if not author:
			raise cherrypy.HTTPRedirect('/author')
		
		note = Note(author, text)
		_notes.append(note)
		note.id = _notes.index(note)
		raise cherrypy.HTTPRedirect('/')
		
#~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

class Author(object):
	@cherrypy.expose
	def index(self):
		return [_header, _author_form, _footer]
	
	@cherrypy.expose
	def set(self, name):
		cherrypy.session['author'] = name
		return [_header, """Hi %s. You can now leave <a href="/" title="Home">notes</a>.""" % (name,), _footer]

#~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

if __name__ == '__main__':
	#define the global configuration settings of CherryPy
	global_conf = {
		'global': 	{	'engine.autoreload.on': False,
									'server.socket_host': 'localhost',
									'server.socket_port': 8080,
								}}
	application_conf = {
		'/style.css': {
			'tools.staticfile.on': True,
			'tools.staticfile.filename': os.path.join(_curdir, 'style.css'),
		}
	}
	
	#update the global CherryPy configuration
	cherrypy.config.update(global_conf)
	
	#create an instance of the application
	note_app = NoteApp()
	
	#attach an instance of the Author class to the main application
	note_app.author = Author()
	
	#mount the application in the '/' base path
	cherrypy.tree.mount(note_app, '/', config = application_conf)
	
	#start the CherryPy HTTP server
	cherrypy.server.start()
	
	#start the CherryPy engine
	cherrypy.engine.start()
