#==========================================================================
# tostdk :: tostlib :: shell_update.py
# Shell update command
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

import shell
import shell_parser
import shell_command
import project


#==========================================================================
def register ( ):
#==========================================================================

	shell.Shell.register_command(ShellUpdate)


#==========================================================================
class ShellUpdate ( shell_command.ShellCommand ):
#==========================================================================

	#----------------------------------------------------------------------
	@classmethod
	def get_name ( cls ):
	#----------------------------------------------------------------------

		return 'update'

	#----------------------------------------------------------------------
	@classmethod
	def get_description ( cls ):
	#----------------------------------------------------------------------

		return 'Update modified files from the current project.'

	#----------------------------------------------------------------------
	@classmethod
	def get_parameters ( cls ):
	#----------------------------------------------------------------------

		return shell_parser.ShellParameters(
		(
			shell_parser.ShellOption(shell_parser.TYPE_BOOL, 'now',
				'n', 'now',
				False, "Synchronize immediately."),
		), None)

	#----------------------------------------------------------------------
	def execute ( self, p_args ):
	#----------------------------------------------------------------------

		l_project = project.Project.open(os.getcwd())

		if l_project == None:
			print "No project found."
			return 1

		if not l_project.update_files():
			print "Can't update files."
			return 1

		if p_args['now']:
			l_project.synchronize(True)

		return 0


#==========================================================================
# End
#==========================================================================
