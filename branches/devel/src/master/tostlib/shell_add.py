#==========================================================================
# tostdk :: tostlib :: shell_add.py
# Shell add command
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

	shell.Shell.register_command(ShellAdd)


#==========================================================================
class ShellAdd ( shell_command.ShellCommand ):
#==========================================================================

	#----------------------------------------------------------------------
	@classmethod
	def get_name ( cls ):
	#----------------------------------------------------------------------

		return 'add'

	#----------------------------------------------------------------------
	@classmethod
	def get_description ( cls ):
	#----------------------------------------------------------------------

		return 'Add files to the current project.'

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
		(	shell_parser.ShellArgument(shell_parser.TYPE_STRING, 'path',
				'List of files to add.'),
		))

	#----------------------------------------------------------------------
	def execute ( self, p_args ):
	#----------------------------------------------------------------------

		if not ('path' in p_args):
			print "No path given."
			return 2

		l_path = p_args['path']

		l_project = project.Project.open(os.getcwd())

		if l_project == None:
			print "No project found."
			return 1

		l_failed = False

		if not isinstance(l_path, list):
			l_path = [l_path]

		for t_path in l_path:
			if not l_project.add_file(t_path):
				print "Can't add", t_path
				l_failed = True

		if l_failed:
			return 1

		if p_args['now']:
			l_project.synchronize(True)

		if l_failed:
			return 1

		return 0


#==========================================================================
# End
#==========================================================================
