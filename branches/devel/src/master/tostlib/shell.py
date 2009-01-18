#==========================================================================
# tostdk :: tostlib :: shell.py
# Tostdk command shell, interactive or not
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


import sys
import optparse
import cmd
import shlex

import version


#==========================================================================
DESCRIPTION = \
"Tobe's ST DevKit - Copyright 2009 Jean-Baptiste Berlioz\n"
#==========================================================================
LICENSE = \
"""
 Tostdk is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 Tostdk is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with Tostdk.  If not, see <http://www.gnu.org/licenses/>.
"""
#==========================================================================
INTRO = DESCRIPTION + LICENSE + \
"""
Type 'help' or '?' to list existing commands.
Type 'exit' to quit.
"""
#==========================================================================
USAGE = \
"""
  %prog [options] [command] [args]
  %prog alone to enter interactive mode."""
#==========================================================================

#==========================================================================
class Shell ( cmd.Cmd ):
#==========================================================================

	s_commands = {}

	#----------------------------------------------------------------------
	@classmethod
	def register_command ( cls, p_command ):
	#----------------------------------------------------------------------

		cls.s_commands[p_command.get_name()] = p_command

	#----------------------------------------------------------------------
	def __init__ ( self ):
	#----------------------------------------------------------------------

		cmd.Cmd.__init__(self)

		self.m_option_parser = self.__create_option_parser()
		self.m_exit_code     = 0

	#----------------------------------------------------------------------
	def main ( self ):
	#----------------------------------------------------------------------

		if len(sys.argv) > 1:
			l_options, l_args = self.m_option_parser.parse_args()
			self.execute_command(l_options, l_args)

		else:
			self.cmdloop()

		sys.exit(self.m_exit_code)

	#----------------------------------------------------------------------
	def execute_command ( self, p_options, p_args ):
	#----------------------------------------------------------------------

		l_name = p_args[0]
		l_args = p_args[1:]

		if not self.s_commands.has_key(l_name):
			print "*** Unknow command: " + l_name
			self.m_exit_code = 2
			return

		l_command = self.s_commands[l_name]

		self.m_exit_code = l_command.execute(p_options, l_args)

	#----------------------------------------------------------------------
	def cmdloop ( self ):
	#----------------------------------------------------------------------

		self.intro  = INTRO
		self.prompt = "[tostdk]$ "

		cmd.Cmd.cmdloop(self)

		self.m_exit_code = 0

	#----------------------------------------------------------------------
	def emptyline ( self ): pass
	#----------------------------------------------------------------------

	#----------------------------------------------------------------------
	def default ( self, p_line ):
	#----------------------------------------------------------------------

		l_argv = shlex.split(p_line)
		l_options, l_args = self.m_option_parser.parse_args(args=l_argv)

		self.execute_command(l_options, l_args)
		return False

	#----------------------------------------------------------------------
	def do_help ( self, p_name ):
	#----------------------------------------------------------------------

		if p_name:
			if self.s_commands.has_key(p_name):
				l_command = self.s_commands[p_name]
				print l_command.get_help()
			else:
				cmd.Cmd.do_help(self, p_name)

		else:
			cmd.Cmd.do_help(self, p_name)
			print ' '.join(self.s_commands.iterkeys())

	#----------------------------------------------------------------------
	def help_help ( self ):
	#----------------------------------------------------------------------

		print
		print "help [cmd]: Print help for a command."
		print "   If no command is given, list all commands."
		print "   Alt syntax: ?cmd"
		print

	#----------------------------------------------------------------------
	def do_shell ( self, p_line ):
	#----------------------------------------------------------------------

		pass

	#----------------------------------------------------------------------
	def help_shell ( self ):
	#----------------------------------------------------------------------

		print
		print "shell cmd [options] [args]: Execute a shell command."
		print "   Alt syntax: !cmd [options] [args]"
		print

	#----------------------------------------------------------------------
	def do_exit ( self, p_args ):
	#----------------------------------------------------------------------

		return True

	#----------------------------------------------------------------------
	def help_exit ( self ):
	#----------------------------------------------------------------------

		print
		print "exit: Exit Tostdk."
		print

	#----------------------------------------------------------------------
	def __create_option_parser ( self ):
	#----------------------------------------------------------------------

		l_parser = optparse.OptionParser(
			prog        = 'tostshell',
			version     = version.LONG_VERSION,
			usage       = USAGE,
			description = DESCRIPTION)

		self.__add_general_options(l_parser)

		for l_command in self.s_commands.itervalues():
			l_group_def = l_command.get_option_group()

			if not l_group_def:
				continue

			l_title = "Options for " + l_command.get_name() + ":"
			l_descr = l_group_def.get_description()

			l_group = optparse.OptionGroup(l_parser, l_title, l_descr)

			for l_option_def in l_group_def.get_options():

				l_default = l_option_def.get_default()
				if isinstance(l_default, bool):
					if l_default:
						l_action = 'store_false'
					else:
						l_action = 'store_true'
				else:
					l_action = 'store'

				l_group.add_option(
					l_option_def.get_short(),
					l_option_def.get_long(),
					action  = l_action,
					dest    = l_option_def.get_destination(),
					default = option_def.get_default(),
					help    = option_def.get_help())

			l_parser.add_option_group(l_group)

		return l_parser

	#----------------------------------------------------------------------
	def __add_general_options ( self, p_parser ):
	#----------------------------------------------------------------------

		pass


#==========================================================================
def main ( ):
#==========================================================================

	l_shell = Shell()
	l_shell.main()


#==========================================================================
# End
#==========================================================================
