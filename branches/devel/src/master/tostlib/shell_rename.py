#==========================================================================
# tostdk :: tostlib :: shell_rename.py
# Shell rename command
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

import project
import shell
import shell_parser
import shell_command


#==========================================================================
def register ( ):
#==========================================================================

	shell.Shell.register_command(ShellRename)


#==========================================================================
class ShellRename ( shell_command.ShellCommand ):
#==========================================================================

	#----------------------------------------------------------------------
	@classmethod
	def get_name ( cls ):
	#----------------------------------------------------------------------

		return 'rename'

	#----------------------------------------------------------------------
	@classmethod
	def get_description ( cls ):
	#----------------------------------------------------------------------

		return 'Rename files from the current project.'

	#----------------------------------------------------------------------
	@classmethod
	def get_parameters ( cls ):
	#----------------------------------------------------------------------

		return shell_parser.ShellParameters(
		(
			shell_parser.ShellOption(shell_parser.TYPE_BOOL, 'now',
				'n', 'now',
				False, "Synchronize immediately."),
		),
		(	shell_parser.ShellArgument(shell_parser.TYPE_STRING, 'from',
				'Name of the file to rename.'),
			shell_parser.ShellArgument(shell_parser.TYPE_STRING, 'to',
				'New file name.')
		))

	#----------------------------------------------------------------------
	def execute ( self, p_args ):
	#----------------------------------------------------------------------

		if not ('from' in p_args):
			print "No file name given."
			return 2

		if not ('to' in p_args):
			print "No new file name given."
			return 2

		l_old = p_args['from']
		l_to  = p_args['to']

		if isinstance(l_to, list):
			print "Too much parameters."
			return 2

		l_project = project.Project.open(os.getcwd())

		if l_project == None:
			print "No project found."
			return 1

		if not l_project.rename_file(l_old, l_new):
			print "Can't rename", l_old, "to", l_new
			return 1

		if p_args['now']:
			l_project.synchronize(True)

		return 0


#==========================================================================
# End
#==========================================================================
