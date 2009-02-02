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

import singleton
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
Type 'exit' or 'quit' to quit.
"""
#==========================================================================
USAGE = DESCRIPTION + LICENSE + \
"""
Usage:
 tostshell [options] [command] [options] [args]
or:
 tostshell alone to enter interactive mode.
"""
#==========================================================================


#==========================================================================
class Shell ( cmd.Cmd, singleton.Singleton ):
#==========================================================================

	s_instance = None
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
		singleton.Singleton.__init__(self)

		self.m_parser      = self.__create_parser()
		self.m_interactive = False
		self.m_exit_code   = 0

	#----------------------------------------------------------------------
	def get_commands   ( self ): return self.s_commands
	def get_parser     ( self ): return self.m_parser
	def is_interactive ( self ): return self.m_interactive
	def get_exit_code  ( self ): return self.m_exit_code
	#----------------------------------------------------------------------

	#----------------------------------------------------------------------
	def main ( self ):
	#----------------------------------------------------------------------

		if len(sys.argv) > 1:
			l_ok,          \
			l_args,        \
			l_command,     \
			l_command_args = self.m_parser.parse(sys.argv[1:])

			if l_ok:
				self.__execute_options(**l_args)
				self.m_exit_code = self.execute_command(l_command, l_command_args)
			else:
				print USAGE
				self.m_exit_code = 2

		else:
			self.m_interactive = True
			self.cmdloop()

		sys.exit(self.m_exit_code)

	#----------------------------------------------------------------------
	def has_command ( self, p_name ):
	#----------------------------------------------------------------------

		return (p_name in self.s_commands)

	#----------------------------------------------------------------------
	def get_command ( self, p_name ):
	#----------------------------------------------------------------------

		return self.s_commands[p_name]

	#----------------------------------------------------------------------
	def execute_cmdline ( self, p_line ):
	#----------------------------------------------------------------------

		l_argv = shlex.split(p_line)

		l_ok,          \
		l_args,        \
		l_command,     \
		l_command_args = self.m_parser.parse(l_argv)

		if not l_ok:
			print 'Unknow command:', p_line
			return 2

		return self.execute_command(l_command, l_command_args)

	#----------------------------------------------------------------------
	def execute_command ( self, p_command, p_args = {} ):
	#----------------------------------------------------------------------

		if not self.s_commands.has_key(p_command):
			print "Unknow command: " + p_command
			return 2

		l_command = self.s_commands[p_command]

		return l_command().execute(p_args)

	#----------------------------------------------------------------------
	def __create_parser ( self ):
	#----------------------------------------------------------------------

		return shell_parser.ShellParser(self.__get_general_parameters(),
										self.__get_commands_parameters())

	#----------------------------------------------------------------------
	def __get_general_parameters ( self ):
	#----------------------------------------------------------------------

		return shell_parser.ShellParameters((
			shell_parser.ShellOption(shell_parser.TYPE_BOOL,
					'usage', '', 'usage', False,
					'Display usage.'),

			shell_parser.ShellOption(shell_parser.TYPE_BOOL,
					'help', '', 'help', False,
					'Display help.'),

			shell_parser.ShellOption(shell_parser.TYPE_BOOL,
					'version', '', 'version', False,
					'Display version.'),

			shell_parser.ShellOption(shell_parser.TYPE_BOOL,
					'license', '', 'license', False,
					'Display license.'),
		))

	#----------------------------------------------------------------------
	def __get_commands_parameters ( self ):
	#----------------------------------------------------------------------

		l_parameters = {}

		for l_name, l_command in self.s_commands.iteritems():
			l_parameters[l_name] = l_command.get_parameters()

		return l_parameters

	#----------------------------------------------------------------------
	def __execute_options ( self, usage, help, version, license ):
	#----------------------------------------------------------------------

		if usage:
			self.execute_cmdline('usage')
			sys.exit(0)

		if help:
			self.execute_cmdline('help')
			sys.exit(0)

		if version:
			self.execute_cmdline('version')
			sys.exit(0)

		if license:
			self.execute_cmdline('license')
			sys.exit(0)

	#======================================================================
	# Interactive mode
	#======================================================================

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

		self.execute_cmdline(p_line)
		return False

	#----------------------------------------------------------------------
	def do_help ( self, p_name ):
	#----------------------------------------------------------------------

		self.execute_cmdline('help ' + p_name)
		return False

	#----------------------------------------------------------------------
	def do_shell ( self, p_line ):
	#----------------------------------------------------------------------

		self.execute_cmdline('shell ' + p_line)
		return False

	#----------------------------------------------------------------------
	def do_exit ( self, p_args = '' ): return True
	def do_quit ( self, p_args = '' ): return True
	#----------------------------------------------------------------------


#==========================================================================
def main ( ):
#==========================================================================

	l_shell = Shell.get_instance()
	l_shell.main()


#==========================================================================
# End
#==========================================================================
