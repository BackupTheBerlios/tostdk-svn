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


import logging


#======================================================================
TYPE_BOOL   = 0
TYPE_INT    = 1
TYPE_FLOAT  = 2
TYPE_STRING = 3
#======================================================================


#======================================================================
class ShellOption:
#======================================================================

	#------------------------------------------------------------------
	def __init__ ( self, p_type, p_name, p_short, p_long, p_default, p_descr ):
	#------------------------------------------------------------------

		self.m_type    = p_type
		self.m_name    = p_name
		self.m_short   = p_short
		self.m_long    = p_long
		self.m_default = p_default
		self.m_descr   = p_descr

	#------------------------------------------------------------------
	def get_type    ( self ): return self.m_type
	def get_name    ( self ): return self.m_name
	def get_short   ( self ): return self.m_short
	def get_long    ( self ): return self.m_long
	def get_default ( self ): return self.m_default
	def get_descr   ( self ): return self.m_descr
	#------------------------------------------------------------------


#======================================================================
class ShellArgument:
#======================================================================

	#------------------------------------------------------------------
	def __init__ ( self, p_type, p_name, p_descr ):
	#------------------------------------------------------------------

		self.m_type  = p_type
		self.m_name  = p_name
		self.m_descr = p_descr

	#------------------------------------------------------------------
	def get_type  ( self ): return self.m_type
	def get_name  ( self ): return self.m_name
	def get_descr ( self ): return self.m_descr
	#------------------------------------------------------------------


#======================================================================
class ShellParameters:
#======================================================================

	#------------------------------------------------------------------
	def __init__ ( self, p_options = None, p_arguments = None ):
	#------------------------------------------------------------------

		self.m_options   = p_options
		self.m_arguments = p_arguments

		if self.m_options == None:
			self.m_options = []

		if self.m_arguments == None:
			self.m_arguments = []

	#------------------------------------------------------------------
	def get_options   ( self ): return self.m_options
	def get_arguments ( self ): return self.m_arguments
	#------------------------------------------------------------------

	#------------------------------------------------------------------
	def get_argument ( self, p_index ):
	#------------------------------------------------------------------

		if not self.m_arguments:
			return None

		if p_index >= len(self.m_arguments):
			return self.m_arguments[-1]

		return self.m_arguments[p_index]

	#------------------------------------------------------------------
	def get_short_option ( self, p_short ):
	#------------------------------------------------------------------

		l_option = None

		for l_option_def in self.m_options:
			if l_option_def.get_short() == p_short:
				l_option = l_option_def
				break

		return l_option

	#------------------------------------------------------------------
	def get_long_option ( self, p_long ):
	#------------------------------------------------------------------

		l_option = None

		for l_option_def in self.m_options:
			if l_option_def.get_long() == p_long:
				l_option = l_option_def
				break

		return l_option


#==========================================================================
class ShellParser:
#==========================================================================

	#----------------------------------------------------------------------
	def __init__ ( self, p_general_parameters, p_commands_parameters ):
	#----------------------------------------------------------------------

		self.m_general_parameters  = p_general_parameters
		self.m_commands_parameters = p_commands_parameters

	#----------------------------------------------------------------------
	def get_general_parameters ( self ):
	#----------------------------------------------------------------------

		return self.m_general_parameters

	#----------------------------------------------------------------------
	def get_command_parameters ( self, p_command ):
	#----------------------------------------------------------------------

		if p_command in self.m_commands_parameters:
			return self.m_commands_parameters[p_command]

		return None

	#----------------------------------------------------------------------
	def parse ( self, p_argv ):
	#----------------------------------------------------------------------

		l_argv = p_argv[:]

		l_general_args = {}
		l_command_args = {}

		l_command    = None
		l_parameters = self.m_general_parameters

		self.set_default_options(l_parameters, l_general_args)

		l_arg_index = 0
		l_ok        = True

		while (l_ok and l_argv):
			l_word = l_argv[0]

			if not l_word:
				continue

			if l_word.startswith('--'):
				if l_command:
					l_ok = self.parse_long_option(l_argv, l_parameters,
													l_command_args)
				else:
					l_ok = self.parse_long_option(l_argv, l_parameters,
													l_general_args)

			elif l_word.startswith('-'):
				if l_command:
					l_ok = self.parse_short_options(l_argv, l_parameters,
													l_command_args)
				else:
					l_ok = self.parse_short_options(l_argv, l_parameters,
													l_general_args)

			elif not l_command:
				if self.m_commands_parameters.has_key(l_word):
					l_command    = l_word
					l_parameters = self.m_commands_parameters[l_word]
					self.set_default_options(l_parameters, l_command_args)
					del l_argv[0]
				else:
					l_ok = False

			else:
				l_ok = self.parse_argument(l_argv, l_parameters, l_arg_index,
													l_command_args)
				l_arg_index += 1

		return (l_ok, l_general_args, l_command, l_command_args)

	#----------------------------------------------------------------------
	def set_default_options ( self, p_parameters, p_args ):
	#----------------------------------------------------------------------

		for l_option_def in p_parameters.get_options():

			l_name    = l_option_def.get_name()
			l_default = l_option_def.get_default()

			p_args[l_name] = l_default

	#----------------------------------------------------------------------
	def parse_short_options ( self, p_argv, p_parameters, p_args ):
	#----------------------------------------------------------------------

		l_string  = p_argv.pop(0)[1:]
		l_has_arg = False

		for l_short in l_string:

			l_short_def = p_parameters.get_short_option(l_short)

			if not l_short_def:
				logging.output('Unknow option: -' + l_short)
				return False

			l_type = l_short_def.get_type()

			if l_type == TYPE_BOOL:
				l_value = not l_short_def.get_default()

			elif not p_argv:
				logging.output('Option -' + l_short + ' need an argument.')
				return False

			elif l_has_arg:
				logging.output('Invalid option string: ' + l_string)
				return False

			else:
				l_arg     = p_argv.pop(0)
				l_value   = self.__from_string(l_type, l_arg)
				l_has_arg = True

			p_args[l_short_def.get_name()] = l_value

		return True

	#----------------------------------------------------------------------
	def parse_long_option ( self, p_argv, p_parameters, p_args ):
	#----------------------------------------------------------------------

		l_long = p_argv.pop(0)[2:]
		l_long_def = p_parameters.get_long_option(l_long)

		if not l_long_def:
			logging.output('Unknow option: --' + l_long)
			return False

		l_type = l_long_def.get_type()

		if l_type == TYPE_BOOL:
			l_value = not l_long_def.get_default()

		elif not p_argv:
			logging.output('Option --' + l_long + ' need an argument.')
			return False

		else:
			l_arg = p_argv.pop(0)
			l_value = self.__from_string(l_type, l_arg)

		p_args[l_long_def.get_name()] = l_value

		return True

	#----------------------------------------------------------------------
	def parse_argument ( self, p_argv, p_parameters, p_index, p_args ):
	#----------------------------------------------------------------------

		l_arg = p_argv.pop(0)
		l_arg_def = p_parameters.get_argument(p_index)

		if not l_arg_def:
			logging.output('Unexpected argument: ' + l_arg)
			return False

		l_name  = l_arg_def.get_name()
		l_value = self.__from_string(l_arg_def.get_type(), l_arg)

		if p_args.has_key(l_name):
			if isinstance(p_args[l_name], list):
				p_args[l_name].append(l_value)
			else:
				p_args[l_name] = [p_args[l_name], l_value]
		else:
			p_args[l_name] = l_value

		return True

	#----------------------------------------------------------------------
	def __from_string ( self, p_type, p_string ):
	#----------------------------------------------------------------------

		if p_type == TYPE_BOOL:
			return [False, True][p_string.lower() in ('true', 'on')]

		elif p_type == TYPE_INT:
			return int(p_string)

		elif p_type == TYPE_FLOAT:
			return float(p_string)

		return p_string


#==========================================================================
# End
#==========================================================================
