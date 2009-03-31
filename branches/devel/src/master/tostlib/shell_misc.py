#==========================================================================
# tostdk :: tostlib :: shell_misc.py
# Misc shell commands
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
import version
import shell
import shell_parser
import shell_command


#==========================================================================
def register ( ):
#==========================================================================

	shell.Shell.register_command(ShellVersion)
	shell.Shell.register_command(ShellUsage)
	shell.Shell.register_command(ShellLicense)
	shell.Shell.register_command(ShellShell)
	shell.Shell.register_command(ShellCd)


#==========================================================================
class ShellVersion ( shell_command.ShellCommand ):
#==========================================================================

	#----------------------------------------------------------------------
	@classmethod
	def get_name ( cls ):
	#----------------------------------------------------------------------

		return 'version'

	#----------------------------------------------------------------------
	@classmethod
	def get_description ( cls ):
	#----------------------------------------------------------------------

		return 'Prints version.'

	#----------------------------------------------------------------------
	def execute ( self, p_args ):
	#----------------------------------------------------------------------

		print
		print version.LONG_VERSION
		print


#==========================================================================
class ShellUsage ( shell_command.ShellCommand ):
#==========================================================================

	#----------------------------------------------------------------------
	@classmethod
	def get_name ( cls ):
	#----------------------------------------------------------------------

		return 'usage'

	#----------------------------------------------------------------------
	@classmethod
	def get_description ( cls ):
	#----------------------------------------------------------------------

		return 'Prints usage.'

	#----------------------------------------------------------------------
	def execute ( self, p_args ):
	#----------------------------------------------------------------------

		print shell.USAGE


#==========================================================================
class ShellLicense ( shell_command.ShellCommand ):
#==========================================================================

	#----------------------------------------------------------------------
	@classmethod
	def get_name ( cls ):
	#----------------------------------------------------------------------

		return 'license'

	#----------------------------------------------------------------------
	@classmethod
	def get_description ( cls ):
	#----------------------------------------------------------------------

		return 'Prints license.'

	#----------------------------------------------------------------------
	def execute ( self, p_args ):
	#----------------------------------------------------------------------

		print shell.LICENSE


#==========================================================================
class ShellShell ( shell_command.ShellCommand ):
#==========================================================================

	#----------------------------------------------------------------------
	@classmethod
	def get_name ( cls ):
	#----------------------------------------------------------------------

		return 'shell'

	#----------------------------------------------------------------------
	@classmethod
	def get_description ( cls ):
	#----------------------------------------------------------------------

		return 'Execute a shell command.'

	#----------------------------------------------------------------------
	@classmethod
	def get_parameters ( cls ):
	#----------------------------------------------------------------------

		return shell_parser.ShellParameters(None, (
			shell_parser.ShellArgument(shell_parser.TYPE_STRING, 'command',
				'Command line.'),
		))

	#----------------------------------------------------------------------
	def execute ( self, p_args ):
	#----------------------------------------------------------------------

		if not ('command' in p_args):
			print "No command to execute."
			return 2

		l_args = p_args['command']

		if isinstance(l_args, list):
			l_cmd = ' '.join(l_args)
		else:
			l_cmd = l_args

		return os.system(l_cmd)


#==========================================================================
class ShellCd ( shell_command.ShellCommand ):
#==========================================================================

	#----------------------------------------------------------------------
	@classmethod
	def get_name ( cls ):
	#----------------------------------------------------------------------

		return 'cd'

	#----------------------------------------------------------------------
	@classmethod
	def get_description ( cls ):
	#----------------------------------------------------------------------

		return 'Change current directory.'

	#----------------------------------------------------------------------
	@classmethod
	def get_parameters ( cls ):
	#----------------------------------------------------------------------

		return shell_parser.ShellParameters(None, (
			shell_parser.ShellArgument(shell_parser.TYPE_STRING, 'directory',
				'New directory.'),
		))

	#----------------------------------------------------------------------
	def execute ( self, p_args ):
	#----------------------------------------------------------------------

		if not ('directory' in p_args):
			print "No directory specified."
			return 2

		l_path = p_args['directory']

		if isinstance(l_path, list):
			print "Unquoted path with spaces."
			return 2

		if os.path.isabs(l_path):
			l_path = os.path.normpath(l_path)

		else:
			l_path = os.path.abspath(l_path)

		if not os.path.exists(l_path):
			print "Path doesn't exists", l_path
			return 1

		try:
			os.chdir(l_path)
		except:
			print "Can't cd to path", l_path
			return 1

		return 0


#==========================================================================
# End
#==========================================================================
