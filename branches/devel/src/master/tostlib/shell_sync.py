#==========================================================================
# tostdk :: tostlib :: shell_sync.py
# Shell sync command
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

	shell.Shell.register_command(ShellSync)


#==========================================================================
class ShellSync ( shell_command.ShellCommand ):
#==========================================================================

	#----------------------------------------------------------------------
	@classmethod
	def get_name ( cls ):
	#----------------------------------------------------------------------

		return 'sync'

	#----------------------------------------------------------------------
	@classmethod
	def get_description ( cls ):
	#----------------------------------------------------------------------

		return 'Synchronize files from the current project.'

	#----------------------------------------------------------------------
	def execute ( self, p_args ):
	#----------------------------------------------------------------------

		l_project = project.Project.open(os.getcwd())

		if l_project == None:
			print "No project found."
			return 1

		l_project.synchronize(True)

		return 0


#==========================================================================
# End
#==========================================================================
