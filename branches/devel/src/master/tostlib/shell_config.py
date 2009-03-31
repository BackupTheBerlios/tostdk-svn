#==========================================================================
# tostdk :: tostlib :: shell_config.py
# Shell configuration commands
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

import configuration
import project
import shell
import shell_parser
import shell_command


#==========================================================================
def register ( ):
#==========================================================================

	shell.Shell.register_command(ShellList)
	shell.Shell.register_command(ShellGet)
	shell.Shell.register_command(ShellSet)


#==========================================================================
class ShellList ( shell_command.ShellCommand ):
#==========================================================================

	#----------------------------------------------------------------------
	@classmethod
	def get_name ( cls ):
	#----------------------------------------------------------------------

		return 'list'

	#----------------------------------------------------------------------
	@classmethod
	def get_description ( cls ):
	#----------------------------------------------------------------------

		return 'List configuration options.'

	#----------------------------------------------------------------------
	@classmethod
	def get_parameters ( cls ):
	#----------------------------------------------------------------------

		return shell_parser.ShellParameters(
		(
			shell_parser.ShellOption(shell_parser.TYPE_BOOL, 'site',
				's', 'site', False,
				"Filter options from site configuration."),
			shell_parser.ShellOption(shell_parser.TYPE_BOOL, 'user',
				'u', 'user', False,
				"Filter options from user configuration."),
			shell_parser.ShellOption(shell_parser.TYPE_BOOL, 'project',
				'p', 'project', False,
				"Filter options from project configuration.")
		),
		(
			shell_parser.ShellArgument(shell_parser.TYPE_STRING, 'section',
				'Section name or nothing to list sections.'),
		))

	#----------------------------------------------------------------------
	def execute ( self, p_args ):
	#----------------------------------------------------------------------

		if 'section' in p_args:
			return self.__list_options(p_args)
		else:
			return self.__list_sections(p_args)

	#----------------------------------------------------------------------
	def __list_options ( self, p_args ):
	#----------------------------------------------------------------------

		l_section = p_args['section']

		l_filter = []

		if p_args['site']:
			l_filter.append(configuration.LEVEL_SITE)

		if p_args['user']:
			l_filter.append(configuration.LEVEL_USER)

		if p_args['project']:
			l_filter.append(configuration.LEVEL_PROJECT)

		if p_args['site'] + p_args['user'] + p_args['project'] == 0:
			l_filter = [
				configuration.LEVEL_SITE,
				configuration.LEVEL_USER,
				configuration.LEVEL_PROJECT
			]

		l_project = project.Project.open(os.getcwd())
		l_config  = configuration.Configuration.get_instance()

		if not l_config.has_section(l_section):
			print "Unknown section", l_section
			return 1

		for l_option in l_config.options_iterator(l_section):
			print l_section + ':' + l_option

		return 0

	#----------------------------------------------------------------------
	def __list_sections ( self, p_args ):
	#----------------------------------------------------------------------

		l_config = configuration.Configuration.get_instance()

		for l_section in l_config.sections_iterator():
			print l_section

		return 0


#==========================================================================
class ShellGet ( shell_command.ShellCommand ):
#==========================================================================

	#----------------------------------------------------------------------
	@classmethod
	def get_name ( cls ):
	#----------------------------------------------------------------------

		return 'get'

	#----------------------------------------------------------------------
	@classmethod
	def get_description ( cls ):
	#----------------------------------------------------------------------

		return 'Retrieve a configuration option.'

	#----------------------------------------------------------------------
	@classmethod
	def get_parameters ( cls ):
	#----------------------------------------------------------------------

		return shell_parser.ShellParameters(None, (
			shell_parser.ShellArgument(shell_parser.TYPE_STRING, 'option',
				'Configuration option name.'),
		))

	#----------------------------------------------------------------------
	def execute ( self, p_args ):
	#----------------------------------------------------------------------

		if not ('option' in p_args):
			print "No option name given."
			return 2

		if isinstance(p_args['option'], list):
			print "Too many parameters."
			return 2

		l_split = p_args['option'].split(':')
		if len(l_split) != 2:
			print "Invalid option name", p_args['option']
			return 1

		l_section, l_option = l_split

		l_project = project.Project.open(os.getcwd())
		l_config  = configuration.Configuration.get_instance()
		l_value   = l_config.get_option_value(l_section, l_option)

		if l_value == None:
			print "Unknown option", p_args['option']
			return 1

		print p_args['option'], '=', str(l_value)

		return 0


#==========================================================================
class ShellSet ( shell_command.ShellCommand ):
#==========================================================================

	#----------------------------------------------------------------------
	@classmethod
	def get_name ( cls ):
	#----------------------------------------------------------------------

		return 'set'

	#----------------------------------------------------------------------
	@classmethod
	def get_description ( cls ):
	#----------------------------------------------------------------------

		return 'Change a configuration option.'

	#----------------------------------------------------------------------
	@classmethod
	def get_parameters ( cls ):
	#----------------------------------------------------------------------

		return shell_parser.ShellParameters(
		(
			shell_parser.ShellOption(shell_parser.TYPE_BOOL, 'site',
				's', 'site', False,
				"Move option to site configuration file."),
			shell_parser.ShellOption(shell_parser.TYPE_BOOL, 'user',
				'u', 'user', False,
				"Move option to user configuration file."),
			shell_parser.ShellOption(shell_parser.TYPE_BOOL, 'project',
				'p', 'project', False,
				"Move option to project configuration file.")
		),
		(
			shell_parser.ShellArgument(shell_parser.TYPE_STRING, 'option',
				'Configuration option name.'),
			shell_parser.ShellArgument(shell_parser.TYPE_STRING, 'value',
				'Configuration option value.')
		))

	#----------------------------------------------------------------------
	def execute ( self, p_args ):
	#----------------------------------------------------------------------

		if not ('option' in p_args):
			print "No option name given."
			return 2

		if not ('value' in p_args):
			print "No value given."
			return 2

		if isinstance(p_args['value'], list):
			print "Too many parameters."
			return 2

		if p_args['site'] + p_args['user'] + p_args['project'] > 1:
			print "An option can only be moved to one configuration file."
			return 2

		l_split = p_args['option'].split(':')
		if len(l_split) != 2:
			print "Invalid option name", p_args['option']
			return 1

		l_section, l_option = l_split
		l_value   = p_args['value']

		l_project = project.Project.open(os.getcwd())
		l_config  = configuration.Configuration.get_instance()

		if not l_config.has_option(l_section, l_option):
			print "Unknown option", p_args['option']
			return 1

		if p_args['site']:
			l_level = configuration.LEVEL_SITE

		elif p_args['user']:
			l_level = configuration.LEVEL_USER

		elif p_args['project']:
			l_level = configuration.LEVEL_PROJECT

		else:
			l_level   = l_config.get_option_level(l_section, l_option)

		if (l_project == None) and (l_level == configuration.LEVEL_PROJECT):
			print "Project options must be set from a project directory."
			return 1

		if not l_config.set_option_string(l_level, l_section, l_option, l_value):
			print "Can't change option", p_args['option']
			return 1

		if l_project:
			l_master_path = l_project.get_master_path()
		else:
			l_master_path = ''

		if not l_config.save(l_master_path):
			print "Can't save configuration."
			return 1

		print p_args['option'], '=', l_value

		return 0


#==========================================================================
# End
#==========================================================================
