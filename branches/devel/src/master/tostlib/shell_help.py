#==========================================================================
# tostdk :: tostlib :: shell_help.py
# Help shell commands
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


import configuration
import shell
import shell_parser
import shell_command


#==========================================================================
def register ( ):
#==========================================================================

	shell.Shell.register_command(ShellHelp)


#==========================================================================
class ShellHelp ( shell_command.ShellCommand ):
#==========================================================================

	#----------------------------------------------------------------------
	@classmethod
	def get_name ( cls ):
	#----------------------------------------------------------------------

		return 'help'

	#----------------------------------------------------------------------
	@classmethod
	def get_description ( cls ):
	#----------------------------------------------------------------------

		return 'Prints help.'

	#----------------------------------------------------------------------
	@classmethod
	def get_parameters ( cls ):
	#----------------------------------------------------------------------

		return shell_parser.ShellParameters(None, (
			shell_parser.ShellArgument(shell_parser.TYPE_STRING, 'command',
				'Command name, option or nothing to list all available commands.'),
		))

	#----------------------------------------------------------------------
	def execute ( self, p_args ):
	#----------------------------------------------------------------------

		if 'command' in p_args:
			l_command = p_args['command']

			if ':' in l_command:
				return self.__help_option(l_command)

			else:
				return self.__help_command(l_command)

		else:
			return self.__list_commands()

	#----------------------------------------------------------------------
	def __help_option ( self, p_command ):
	#----------------------------------------------------------------------

		l_split = p_command.split(':')
		if len(l_split) != 2:
			print "Invalid option name", p_command
			return 1

		l_section, l_option = l_split

		l_config = configuration.Configuration.get_instance()
		l_desc   = l_config.get_option_desc(l_section, l_option)
		l_type   = l_config.get_option_type(l_section, l_option)

		if not l_desc:
			print "Unknown option", p_command
			return 1

		print
		print p_command, ':', l_desc, '(' + l_type['desc'] + ')'
		print

		return 0


	#----------------------------------------------------------------------
	def __help_command ( self, p_command ):
	#----------------------------------------------------------------------

		l_shell = shell.Shell.get_instance()

		if not l_shell.has_command(p_command):
			print 'Unknow command:', p_command
			return 2

		l_command = l_shell.get_command(p_command)
		l_params  = l_shell.get_parser().get_command_parameters(p_command)
		l_options = l_params.get_options()
		l_args    = l_params.get_arguments()

		print '\n' + l_command.get_description()

		l_usage = ' ' + l_command.get_name()
		if l_options:
			l_usage += ' [options]'
		if l_args:
			for l_arg in l_args:
				l_usage += ' ' + l_arg.get_name()

		print '\nUsage:\n'
		print l_usage

		if l_options:
			print '\nOptions:\n'
			for l_opt in l_options:
				print ' -' + l_opt.get_short() + ', --' + l_opt.get_long() + \
					' : ' + l_opt.get_descr() + \
					' (default = ' + str(l_opt.get_default()) + ')'

		if l_args:
			print '\nArguments:\n'
			for l_arg in l_args:
				print ' ' + l_arg.get_name() + ' : ' + l_arg.get_descr()

		print
		return 0

	#----------------------------------------------------------------------
	def __list_commands ( self ):
	#----------------------------------------------------------------------

		l_shell    = shell.Shell.get_instance()
		l_commands = l_shell.get_commands()

		print
		for l_name, l_command in sorted(l_commands.iteritems()):
			print ' ' + l_name + ':', l_command.get_description()
		print

		return 0


#==========================================================================
# End
#==========================================================================
