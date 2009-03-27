#==========================================================================
# tostdk :: tostlib :: shell_create.py
# Project creation shell command
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


import shell
import shell_parser
import shell_command
import project


#==========================================================================
def register ( ):
#==========================================================================

	shell.Shell.register_command(ShellCreate)


#==========================================================================
class ShellCreate ( shell_command.ShellCommand ):
#==========================================================================

	#----------------------------------------------------------------------
	@classmethod
	def get_name ( cls ):
	#----------------------------------------------------------------------

		return 'create'

	#----------------------------------------------------------------------
	@classmethod
	def get_description ( cls ):
	#----------------------------------------------------------------------

		return 'Create a new project in the current directory.'

	#----------------------------------------------------------------------
	@classmethod
	def get_parameters ( cls ):
	#----------------------------------------------------------------------

		return shell_parser.ShellParameters(None, (
			shell_parser.ShellArgument(shell_parser.TYPE_STRING, 'masterpath',
				'Local path.'),
			shell_parser.ShellArgument(shell_parser.TYPE_STRING, 'slavepath',
				'Remote path.'),
		))

	#----------------------------------------------------------------------
	def execute ( self, p_args ):
	#----------------------------------------------------------------------

		if not ('masterpath' in p_args):
			print "No local path given."
			return 2

		if not ('slavepath' in p_args):
			print "No remote path given."
			return 2

		l_master_path = p_args['masterpath']

		l_root_path = project.Project.find_project_root(l_master_path)
		if l_root_path:
			print "A project already exists in", l_root_path
			return 1

		l_slave_path  = p_args['slavepath']

		l_project = project.Project.create(l_master_path, l_slave_path)

		if l_project == None:
			print "An error occured while creating the project."
			return 1

		return 0


#==========================================================================
# End
#==========================================================================
