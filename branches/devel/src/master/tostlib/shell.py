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
import cmd
import shlex

import version
import shell_parser


#==========================================================================
DESCRIPTION = \
"""
Tobe's ST DevKit - Copyright 2009 Jean-Baptiste Berlioz
"""
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

		self.m_parser    = self.__create_parser()
		self.m_exit_code = 0

	#----------------------------------------------------------------------
	def main ( self ):
	#----------------------------------------------------------------------

		if len(sys.argv) > 1:
			l_ok,          \
			l_args,        \
			l_command,     \
			l_command_args = self.m_parser.parse_args(sys.argv[1:])

			if l_ok:
				self.__execute_options(*l_args)
				self.__execute_command(l_command, l_command_args)

		else:
			self.cmdloop()

		sys.exit(self.m_exit_code)

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

		l_ok,          \
		l_args,        \
		l_command,     \
		l_command_args = self.m_parser.parse_args(l_argv)

		if l_ok:
			self.__execute_command(l_command, *l_command_args)

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
	def __execute_options ( self, show_help=False, show_version=False, show_license=False ):
	#----------------------------------------------------------------------

		pass

	#----------------------------------------------------------------------
	def __execute_command ( p_command, p_args ):
	#----------------------------------------------------------------------

		if not self.s_commands.has_key(p_command):
			print "*** Unknow command: " + p_command
			self.m_exit_code = 2
			return

		l_command = self.s_commands[p_command]

		self.m_exit_code = l_command.execute(*p_args)

	#----------------------------------------------------------------------
	def __create_parser ( self ):
	#----------------------------------------------------------------------

		return None

	#----------------------------------------------------------------------
	def __get_general_parameters ( self ):
	#----------------------------------------------------------------------

		pass

	#----------------------------------------------------------------------
	def __get_commands_parameters ( self ):
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
