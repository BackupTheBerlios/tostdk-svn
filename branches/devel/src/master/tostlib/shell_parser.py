#==========================================================================
# tostdk :: tostlib :: shell_parser.py
# Shell command parser
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


#======================================================================
TYPE_BOOL   = 0
TYPE_INT    = 1
TYPE_FLOAT  = 2
TYPE_STRING = 3
#======================================================================


#======================================================================
def __from_string ( p_type, p_string ):
#======================================================================

	if p_type == TYPE_BOOL:
		return [False, True][p_string.lower() in ('true', 'on')]

	elif p_type == TYPE_INT:
		return int(p_string)

	elif p_type == TYPE_FLOAT:
		return float(p_string)

	return p_string

#======================================================================
def __to_string ( p_type, p_value ):
#======================================================================

	return str(p_value)

#======================================================================
class ShellOption:
#======================================================================

	#------------------------------------------------------------------
	def __init__ ( self, p_type, p_name, p_short, p_long, p_default, p_help )
	#------------------------------------------------------------------

		self.m_type    = p_type
		self.m_name    = p_name
		self.m_short   = p_short
		self.m_long    = p_long
		self.m_default = p_default
		self.m_help    = p_help

	#------------------------------------------------------------------
	def get_type    ( self ): return self.m_type
	def get_name    ( self ): return self.m_name
	def get_short   ( self ): return self.m_short
	def get_long    ( self ): return self.m_long
	def get_default ( self ): return self.m_default
	def get_help    ( self ): return self.m_help
	#------------------------------------------------------------------

#======================================================================
class ShellArgument:
#======================================================================

	#------------------------------------------------------------------
	def __init__ ( self, p_type, p_name, p_required ):
	#------------------------------------------------------------------

		self.m_type = p_type
		self.m_name = p_name

	#------------------------------------------------------------------
	def get_type ( self ): return self.m_type
	def get_name ( self ): return self.m_name
	#------------------------------------------------------------------

#======================================================================
class ShellParameters:
#======================================================================

	#------------------------------------------------------------------
	def __init__ ( self, p_options = {}, p_arguments = [] ):
	#------------------------------------------------------------------

		self.m_options     = p_options
		self.m_arguments   = p_arguments

	#------------------------------------------------------------------
	def get_options ( self ): return self.m_options
	#------------------------------------------------------------------

	#------------------------------------------------------------------
	def get_argument ( self, p_index ):
	#------------------------------------------------------------------

		if p_index >= len(self.m_arguments):
			return None

		return self.m_arguments[p_index]

	#------------------------------------------------------------------
	def get_short_option ( self, p_short ):
	#------------------------------------------------------------------

		l_option = None

		for l_option_def in self.m_options:
			if l_option_def.get_short() == p_short:
				break

		return l_option

	#------------------------------------------------------------------
	def get_long_option ( self, p_long ):
	#------------------------------------------------------------------

		l_option = None

		for l_option_def in self.m_options:
			if l_option_def.get_long() == p_long:
				break

		return l_option

#==========================================================================
class ShellParser:
#==========================================================================

	#----------------------------------------------------------------------
	def __init__ ( self, p_general_parameters ):
	#----------------------------------------------------------------------

		self.m_general_parameters = p_general_parameters

	#----------------------------------------------------------------------
	def parse ( self, p_commands_parameters, p_argv ):
	#----------------------------------------------------------------------

		l_argv = p_argv[:]

		l_general_options   = {}
		l_command_options   = {}
		l_command_arguments = []

		l_command    = None
		l_parameters = self.m_general_parameters

		self.set_default_options(l_parameters, l_general_options)

		l_arg_index = 0
		l_ok        = True

		while (l_ok and l_argv):
			l_word = l_argv[0]

			if not l_word:
				continue

			if l_word.beginswith('--'):
				if l_command:
					l_ok = self.parse_long_option(l_argv, l_parameters,
													l_command_options)
				else:
					l_ok = self.parse_long_option(l_argv, l_parameters,
													l_general_options)

			elif l_word.beginswith('-'):
				if l_command:
					l_ok = self.parse_short_options(l_argv, l_parameters,
													l_command_options)
				else:
					l_ok = self.parse_short_options(l_argv, l_parameters,
													l_general_options)

			elif not l_command:
				if p_commands_parameters.has_key(l_word):
					l_command    = l_word
					l_parameters = p_commands_parameters[l_word]
					self.set_default_options(l_parameters, l_command_options)
					del l_argv[0]
				else:
					l_ok = False

			else:
				l_ok = self.parse_argument(l_argv, l_parameters, l_arg_index
													l_command_arguments)
				l_arg_index += 1

		return (l_ok, l_general_options,
					l_command, l_command_options, l_command_arguments)

	#----------------------------------------------------------------------
	def set_default_options ( self, p_parameters, p_options ):
	#----------------------------------------------------------------------

		for l_option_def in p_parameters.get_options():

			l_name    = l_option_def.get_name()
			l_default = l_option_def.get_default()

			p_options[l_name] = l_default

	#----------------------------------------------------------------------
	def parse_short_options ( self, p_argv, p_parameters, p_options ):
	#----------------------------------------------------------------------

		pass

	#----------------------------------------------------------------------
	def parse_long_option ( self, p_argv, p_parameters, p_options ):
	#----------------------------------------------------------------------

		pass

	#----------------------------------------------------------------------
	def parse_argument ( self, p_argv, p_parameters, p_index, p_arguments ):
	#----------------------------------------------------------------------

		pass

#==========================================================================
# End
#==========================================================================
