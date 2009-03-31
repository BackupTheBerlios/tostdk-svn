#==========================================================================
# tostdk :: tostlib :: configuration.py
# Configuration manager
#--------------------------------------------------------------------------
# Copyright 2009 Jean-Baptiste Berlioz
#--------------------------------------------------------------------------
# This file is part of Tostdk.
#
# Tostdk is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tostdk is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Tostdk.  If not, see <http://www.gnu.org/licenses/>.
#==========================================================================


import os
import sys

import logging
import singleton


#==========================================================================
if sys.platform == 'win32':
	SITE_CONFIG_FILENAME = 'C:\\tostdk.cnf'
	USER_CONFIG_FILENAME = '~\\tostdk.cnf'
else:
	SITE_CONFIG_FILENAME = '/usr/local/etc/tostdk.cnf'
	USER_CONFIG_FILENAME = '~/.tostdk.cnf'
#==========================================================================


#==========================================================================
LEVEL_SITE    = 0	# option is defined in site configuration
LEVEL_USER    = 1	# option is definied in user configuration
LEVEL_PROJECT = 2	# option is defined in project configuration
#==========================================================================


#==========================================================================
TYPE_INT = {
#==========================================================================
	'desc' : "Integer",
	'valid': lambda x: x.isdigit(),
	'read' : lambda x: int(x),
	'write': lambda x: str(x)
}

#==========================================================================
TYPE_BOOL = {
#==========================================================================
	'desc' : "Boolean",
	'enum' : ('false', 'true'),
	'valid': lambda x: x.lower() in ('false', 'true'),
	'read' : lambda x: x.lower() == 'true',
	'write': lambda x: ['false','true'][bool(x)]
}

#==========================================================================
TYPE_STRING = {
#==========================================================================
	'desc' : "String",
	'valid': lambda x: True,
	'read' : lambda x: str(x),
	'write': lambda x: str(x)
}

#==========================================================================
TYPE_VALID_STRING = {
#==========================================================================
	'desc' : "Non empty string",
	'valid': lambda x: x,
	'read' : lambda x: str(x),
	'write': lambda x: str(x)
}

#==========================================================================
CONFIGURATION = {
#==========================================================================

	#----------------------------------------------------------------------
	'general': {
	#----------------------------------------------------------------------

		#------------------------------------------------------------------
		'debug': {
		#------------------------------------------------------------------
			'level'  : LEVEL_SITE,
			'desc'   : "Debug mode",
			'type'   : TYPE_BOOL,
			'default': True
		},

		#------------------------------------------------------------------
		'verbose': {
		#------------------------------------------------------------------
			'level'  : LEVEL_SITE,
			'desc'   : "Verbose mode",
			'type'   : TYPE_BOOL,
			'default': True
		},

		#------------------------------------------------------------------
		'project_dir': {
		#------------------------------------------------------------------
			'level'  : LEVEL_SITE,
			'desc'   : "Project sub-directory",
			'type'   : TYPE_STRING,
			'default': ".tostdk"
		}
	},

	#----------------------------------------------------------------------
	'drivers': {
	#----------------------------------------------------------------------

		#------------------------------------------------------------------
		'driver_name': {
		#------------------------------------------------------------------
			'level'  : LEVEL_SITE,
			'desc'   : "Driver name",
			'type'   : TYPE_VALID_STRING,
			'default': "files_driver"
		},

		#------------------------------------------------------------------
		'files_driver.input': {
		#------------------------------------------------------------------
			'level'  : LEVEL_SITE,
			'desc'   : "File driver input file",
			'type'   : TYPE_VALID_STRING,
			'default': "tostdk.input"
		},

		#------------------------------------------------------------------
		'files_driver.output': {
		#------------------------------------------------------------------
			'level'  : LEVEL_SITE,
			'desc'   : "File driver output file",
			'type'   : TYPE_VALID_STRING,
			'default': "tostdk.output"
		},

		#------------------------------------------------------------------
		'pipes_driver.command': {
		#------------------------------------------------------------------
			'level'  : LEVEL_SITE,
			'desc'   : "Command to execute",
			'type'   : TYPE_VALID_STRING,
			'default': ""
		}
	},

	#----------------------------------------------------------------------
	'project': {
	#----------------------------------------------------------------------

		#------------------------------------------------------------------
		'slave_path': {
		#------------------------------------------------------------------
			'level'  : LEVEL_PROJECT,
			'desc'   : "Remote path",
			'type'   : TYPE_VALID_STRING,
			'default': ""
		}
	},

	#----------------------------------------------------------------------
	'protocol': {
	#----------------------------------------------------------------------

		#------------------------------------------------------------------
		'packet_size': {
		#------------------------------------------------------------------
			'level'  : LEVEL_SITE,
			'desc'   : "Maximum packet data size",
			'type'   : TYPE_INT,
			'default': 4096
		},

		#------------------------------------------------------------------
		'ping_timeout': {
		#------------------------------------------------------------------
			'level'  : LEVEL_SITE,
			'desc'   : "Ping command timeout",
			'type'   : TYPE_INT,
			'default': 2
		},

		#------------------------------------------------------------------
		'chroot_timeout': {
		#------------------------------------------------------------------
			'level'  : LEVEL_SITE,
			'desc'   : "Chroot command timeout",
			'type'   : TYPE_INT,
			'default': 10
		},

		#------------------------------------------------------------------
		'mv_timeout': {
		#------------------------------------------------------------------
			'level'  : LEVEL_SITE,
			'desc'   : "Mv command timeout",
			'type'   : TYPE_INT,
			'default': 10
		},

		#------------------------------------------------------------------
		'rm_timeout': {
		#------------------------------------------------------------------
			'level'  : LEVEL_SITE,
			'desc'   : "Rm command timeout",
			'type'   : TYPE_INT,
			'default': 10
		},

		#------------------------------------------------------------------
		'malloc_timeout': {
		#------------------------------------------------------------------
			'level'  : LEVEL_SITE,
			'desc'   : "Malloc command timeout",
			'type'   : TYPE_INT,
			'default': 2
		},

		#------------------------------------------------------------------
		'free_timeout': {
		#------------------------------------------------------------------
			'level'  : LEVEL_SITE,
			'desc'   : "Free command timeout",
			'type'   : TYPE_INT,
			'default': 2
		},

		#------------------------------------------------------------------
		'download_timeout': {
		#------------------------------------------------------------------
			'level'  : LEVEL_SITE,
			'desc'   : "Download command timeout",
			'type'   : TYPE_INT,
			'default': 120
		},

		#------------------------------------------------------------------
		'unpack_timeout': {
		#------------------------------------------------------------------
			'level'  : LEVEL_SITE,
			'desc'   : "Unpack command timeout",
			'type'   : TYPE_INT,
			'default': 10
		},

		#------------------------------------------------------------------
		'open_timeout': {
		#------------------------------------------------------------------
			'level'  : LEVEL_SITE,
			'desc'   : "Open command timeout",
			'type'   : TYPE_INT,
			'default': 10
		},

		#------------------------------------------------------------------
		'create_timeout': {
		#------------------------------------------------------------------
			'level'  : LEVEL_SITE,
			'desc'   : "Create command timeout",
			'type'   : TYPE_INT,
			'default': 10
		},

		#------------------------------------------------------------------
		'seek_timeout': {
		#------------------------------------------------------------------
			'level'  : LEVEL_SITE,
			'desc'   : "Seek command timeout",
			'type'   : TYPE_INT,
			'default': 10
		},

		#------------------------------------------------------------------
		'read_timeout': {
		#------------------------------------------------------------------
			'level'  : LEVEL_SITE,
			'desc'   : "Read command timeout",
			'type'   : TYPE_INT,
			'default': 120
		},

		#------------------------------------------------------------------
		'write_timeout': {
		#------------------------------------------------------------------
			'level'  : LEVEL_SITE,
			'desc'   : "Write command timeout",
			'type'   : TYPE_INT,
			'default': 120
		},

		#------------------------------------------------------------------
		'close_timeout': {
		#------------------------------------------------------------------
			'level'  : LEVEL_SITE,
			'desc'   : "Close command timeout",
			'type'   : TYPE_INT,
			'default': 60
		}
	}
}
#==========================================================================


#==========================================================================
class Configuration ( singleton.Singleton ):
#==========================================================================

	s_instance = None

	#----------------------------------------------------------------------
	def __init__ ( self ):
	#----------------------------------------------------------------------

		singleton.Singleton.__init__(self)

		self.m_site_filename = self.__find_site_configuration()
		self.m_user_filename = self.__find_user_configuration()

		self.m_sections = {}

	#----------------------------------------------------------------------
	def load ( self, p_project_path = '' ):
	#----------------------------------------------------------------------

		self.m_sections = {}

		if self.m_site_filename:
			logging.message('Loading site configuration from ' + self.m_site_filename)
			if not self.__load_configuration(LEVEL_SITE, self.m_site_filename):
				return False

		if self.m_user_filename:
			logging.message('Loading user configuration from ' + self.m_user_filename)
			if not self.__load_configuration(LEVEL_USER, self.m_user_filename):
				return False

		if p_project_path:
			l_filename = self.__find_project_configuration(p_project_path)
			if os.path.exists(l_filename):
				logging.message('Loading project configuration from ' + l_filename)
				if not self.__load_configuration(LEVEL_PROJECT, l_filename):
					return False

		return True

	#----------------------------------------------------------------------
	def save ( self, p_project_path = '' ):
	#----------------------------------------------------------------------

		if self.m_site_filename:
			logging.message('Saving site configuration to ' + self.m_site_filename)
			if not self.__save_configuration(LEVEL_SITE, self.m_site_filename):
				return False

		if self.m_user_filename:
			logging.message('Saving user configuration to ' + self.m_user_filename)
			if not self.__save_configuration(LEVEL_USER, self.m_user_filename):
				return False

		if p_project_path:
			l_filename = self.__find_project_configuration(p_project_path)
			logging.message('Saving project configuration to ' + l_filename)
			if not self.__save_configuration(LEVEL_PROJECT, l_filename):
				return False

		return True

	#----------------------------------------------------------------------
	def sections_iterator ( self ):
	#----------------------------------------------------------------------

		return CONFIGURATION.iterkeys()

	#----------------------------------------------------------------------
	def has_section ( self, p_section ):
	#----------------------------------------------------------------------

		return CONFIGURATION.has_key(p_section.lower())

	#----------------------------------------------------------------------
	def options_iterator ( self, p_section ):
	#----------------------------------------------------------------------

		l_section = p_section.lower()

		if not CONFIGURATION.has_key(l_section):
			logging.error('Unknow configuration section ' + p_section)
			return None

		return CONFIGURATION[l_section].iterkeys()

	#----------------------------------------------------------------------
	def has_option ( self, p_section, p_option ):
	#----------------------------------------------------------------------

		l_section = p_section.lower()
		l_option  = p_option.lower()

		return CONFIGURATION.has_key(l_section) and \
			   CONFIGURATION[l_section].has_key(l_option)

	#----------------------------------------------------------------------
	def get_option_value ( self, p_section, p_option ):
	#----------------------------------------------------------------------

		l_section = p_section.lower()
		l_option  = p_option.lower()

		if self.m_sections.has_key(l_section) and \
		   self.m_sections[l_section].has_key(l_option):
		   	return self.m_sections[l_section][l_option]['value']

		return self.get_option_default(l_section, l_option)

	#----------------------------------------------------------------------
	def get_option_default ( self, p_section, p_option ):
	#----------------------------------------------------------------------

		l_section = p_section.lower()
		l_option  = p_option.lower()

		if not CONFIGURATION.has_key(l_section):
			logging.error('Unknow configuration section ' + p_section)
			return None

		if not CONFIGURATION[l_section].has_key(l_option):
			logging.error('Unknow configuration option ' + p_option)
			return None

		return CONFIGURATION[l_section][l_option]['default']

	#----------------------------------------------------------------------
	def get_option_desc ( self, p_section, p_option ):
	#----------------------------------------------------------------------

		l_section = p_section.lower()
		l_option  = p_option.lower()

		if not CONFIGURATION.has_key(l_section):
			logging.error('Unknow configuration section ' + p_section)
			return None

		if not CONFIGURATION[l_section].has_key(l_option):
			logging.error('Unknow configuration option ' + p_option)
			return None

		if CONFIGURATION[l_section][l_option].has_key('desc'):
			return CONFIGURATION[l_section][l_option]['desc']

		return ''

	#----------------------------------------------------------------------
	def get_option_type ( self, p_section, p_option ):
	#----------------------------------------------------------------------

		l_section = p_section.lower()
		l_option  = p_option.lower()

		if not CONFIGURATION.has_key(l_section):
			logging.error('Unknow configuration section ' + p_section)
			return None

		if not CONFIGURATION[l_section].has_key(l_option):
			logging.error('Unknow configuration option ' + p_option)
			return None

		if CONFIGURATION[l_section][l_option].has_key('type'):
			return CONFIGURATION[l_section][l_option]['type']

		return ''

	#----------------------------------------------------------------------
	def get_option_enum ( self, p_section, p_option ):
	#----------------------------------------------------------------------

		l_section = p_section.lower()
		l_option  = p_option.lower()

		if not CONFIGURATION.has_key(l_section):
			logging.error('Unknow configuration section ' + p_section)
			return None

		if not CONFIGURATION[l_section].has_key(l_option):
			logging.error('Unknow configuration option ' + p_option)
			return None

		if CONFIGURATION[l_section][l_option].has_key('enum'):
			return CONFIGURATION[l_section][l_option]['enum']

		return tuple()

	#----------------------------------------------------------------------
	def get_option_level ( self, p_section, p_option ):
	#----------------------------------------------------------------------

		l_section = p_section.lower()
		l_option  = p_option.lower()

		if self.m_sections.has_key(l_section) and \
		   self.m_sections[l_section].has_key(l_option):
			return self.m_sections[l_section][l_option]['level']

		return self.get_option_default_level(p_section, p_option)

	#----------------------------------------------------------------------
	def get_option_default_level ( self, p_section, p_option ):
	#----------------------------------------------------------------------

		l_section = p_section.lower()
		l_option  = p_option.lower()

		if not CONFIGURATION.has_key(l_section):
			logging.error('Unknow configuration section ' + p_section)
			return None

		if not CONFIGURATION[l_section].has_key(l_option):
			logging.error('Unknow configuration option ' + p_option)
			return None

		return CONFIGURATION[l_section][l_option]['level']

	#----------------------------------------------------------------------
	def set_option_value ( self, p_level, p_section, p_option, p_value ):
	#----------------------------------------------------------------------

		l_section = p_section.lower()
		l_option  = p_option.lower()

		if not CONFIGURATION.has_key(l_section):
			logging.error('Unknow configuration section ' + p_section)
			return False

		if not CONFIGURATION[l_section].has_key(l_option):
			logging.error('Unknow configuration option ' + p_option)
			return False

		if not self.m_sections.has_key(l_section):
			self.m_sections[l_section] = {}

		self.m_sections[l_section][l_option] = {'level':p_level,'value':p_value}

		return True

	#----------------------------------------------------------------------
	def set_option_string ( self, p_level, p_section, p_option, p_string ):
	#----------------------------------------------------------------------

		l_section = p_section.lower()
		l_option  = p_option.lower()

		if not CONFIGURATION.has_key(l_section):
			logging.error('Unknow configuration section ' + p_section)
			return False

		if not CONFIGURATION[l_section].has_key(l_option):
			logging.error('Unknow configuration option ' + p_option)
			return False

		l_type = CONFIGURATION[l_section][l_option]['type']

		if not l_type['valid'](p_string):
			logging.error('Invalid string: ' + p_string)
			return False

		l_value = l_type['read'](p_string)

		return self.set_option_value(p_level, p_section, p_option, l_value)

	#----------------------------------------------------------------------
	def __find_site_configuration ( self ):
	#----------------------------------------------------------------------

		return SITE_CONFIG_FILENAME

	#----------------------------------------------------------------------
	def __find_user_configuration ( self ):
	#----------------------------------------------------------------------

		return os.path.expanduser(USER_CONFIG_FILENAME)

	#----------------------------------------------------------------------
	def __find_project_configuration ( self, p_project_path ):
	#----------------------------------------------------------------------

		l_project_dir = self.get_option_value('general', 'project_dir')
		l_filename    = os.path.join(p_project_path, l_project_dir, 'config')
		return l_filename

	#----------------------------------------------------------------------
	def __load_configuration ( self, p_level, p_filename ):
	#----------------------------------------------------------------------

		try:
			l_handle = open(p_filename, 'rU')
		except:
			logging.warning("Can't open file: " + p_filename)
			return True

		l_section = ''
		l_skip    = False

		for l_raw_line in l_handle:
			l_line = l_raw_line.strip().lower()

			if not l_line:
				continue

			if l_line[0] == '#':
				continue

			if '[' in l_line:
				l_beg = l_line.find('[')
				l_end = l_line.rfind(']')

				if l_beg == -1 or l_end == -1:
					l_skip = True
					logging.error('Malformed configuration section: ' + l_line + ' in ' + p_filename)
					continue

				l_section = l_line[l_beg+1:l_end].lower()

				if not l_section:
					l_skip = True
					logging.error('Malformed configuration section: ' + l_line + ' in ' + p_filename)
					continue

				if not CONFIGURATION.has_key(l_section):
					l_skip = True
					logging.error('Unknow configuration section: ' + l_section + ' in ' + p_filename)
					continue

				l_skip = False

				if not self.m_sections.has_key(l_section):
					self.m_sections[l_section] = {}

			elif not l_skip:
				l_split = map(lambda x: x.strip().lower(), l_line.split('='))

				if len(l_split) != 2:
					logging.error('Malformed configuration option: ' + l_line + ' in ' + p_filename)
					continue

				l_option, l_string = l_split

				if not CONFIGURATION[l_section].has_key(l_option):
					logging.error('Unknow configuration option: ' + l_option + ' in ' + p_filename)
					continue

				l_type = CONFIGURATION[l_section][l_option]['type']

				if not l_type['valid'](l_string):
					logging.error('Invalid configuration option: ' + l_option + ' in ' + p_filename)
					continue

				l_value = l_type['read'](l_string)

				self.m_sections[l_section][l_option] = {'level':p_level,'value':l_value}

		l_handle.close()
		return True

	#----------------------------------------------------------------------
	def __save_configuration ( self, p_level, p_filename ):
	#----------------------------------------------------------------------

		try:
			l_handle = open(p_filename, 'wb')
		except:
			logging.warning("Can't create file: " + p_filename)
			return True

		for l_section in self.m_sections.iterkeys():
			l_section_started = False

			for l_option in self.m_sections[l_section].iterkeys():

				if self.m_sections[l_section][l_option]['level'] != p_level:
					continue

				if not l_section_started:
					l_handle.write('[' + l_section + ']' + os.linesep)
					l_section_started = True

				if CONFIGURATION[l_section][l_option].has_key('desc'):
					l_desc = CONFIGURATION[l_section][l_option]['desc']
					l_handle.write('# ' + l_desc + os.linesep)

				l_type   = CONFIGURATION[l_section][l_option]['type']
				l_string = l_type['write'](self.m_sections[l_section][l_option]['value'])
				l_handle.write(l_option + ' = ' + l_string + os.linesep)

			if l_section_started:
				l_handle.write(os.linesep)

		l_handle.close()
		return True


#==========================================================================
# End
#==========================================================================
