#==========================================================================
# tostdk :: tostlib :: project.py
# Project manager
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
import sys

import logging
import configuration
import cache


#==========================================================================
class Project:
#==========================================================================

	#----------------------------------------------------------------------
	def __init__ ( self, p_master_path ):
	#----------------------------------------------------------------------

		self.m_master_path = p_master_path

	#----------------------------------------------------------------------
	@classmethod
	def find_project_root ( cls, p_path ):
	#----------------------------------------------------------------------

		l_config = configuration.Configuration.get_instance()

		if not l_config.load():
			return None

		l_project_dir = l_config.get_option_value('general', 'project_dir')
		l_path = os.path.abspath(p_path)

		while l_path:
			l_project_path = os.path.join(l_path, l_project_dir)

			if os.path.exists(l_project_path):
				break

			l_parent = os.path.dirname(l_path)

			if l_parent == l_path:
				l_path = ''
			else:
				l_path = l_parent

		return l_path

	#----------------------------------------------------------------------
	@classmethod
	def open ( cls, p_master_path ):
	#----------------------------------------------------------------------

		l_master_path = cls.find_project_root(p_master_path)

		l_config = configuration.Configuration.get_instance()

		if not l_config.load(l_master_path):
			return None

		return cls(l_master_path)

	#----------------------------------------------------------------------
	@classmethod
	def create ( cls, p_master_path, p_slave_path ):
	#----------------------------------------------------------------------

		l_master_path = os.path.abspath(p_master_path)

		l_config = configuration.Configuration.get_instance()

		if not l_config.load(l_master_path):
			return None

		l_project_dir  = l_config.get_option_value('general', 'project_dir')
		l_project_path = os.path.join(l_master_path, l_project_dir)
		l_cache_path   = os.path.join(l_project_path, 'cache')

		if not os.path.exists(l_project_path):
			try:
				os.makedirs(l_project_path)
			except:
				logging.error("Can't create directory: ", l_project_path)
				return None

		if not os.path.exists(l_cache_path):
			try:
				os.makedirs(l_cache_path)
			except:
				logging.error("Can't create directory: ", l_cache_path)
				return None

		if not l_config.set_option_value('project', 'slave_path', p_slave_path):
			return None

		if not l_config.save(l_master_path):
			return None

		return cls(l_master_path)

	#----------------------------------------------------------------------
	def add_file ( self, p_file_path ):
	#----------------------------------------------------------------------

		l_file_path = os.path.abspath(p_file_path)

		if not l_file_path.startswith(self.m_master_path):
			logging.error("File isn't inside project root: " + l_file_path)
			return False

		if not os.path.exists(l_file_path):
			logging.error("File doesn't exists: ", l_file_path)
			return False

		#TODO: write action

		return False

	#----------------------------------------------------------------------
	def remove_file ( self, p_file_path ):
	#----------------------------------------------------------------------

		l_file_path = os.path.abspath(p_file_path)

		if not l_file_path.startswith(self.m_master_path):
			logging.error("File isn't inside project base: " + l_file_path)
			return False

		if not os.path.exists(l_file_path):
			logging.error("File doesn't exists: ", l_file_path)
			return False

		#TODO: write action

		return False

	#----------------------------------------------------------------------
	def rename_file ( self, p_old_path, p_new_path ):
	#----------------------------------------------------------------------

		l_old_path = os.path.abspath(p_old_path)
		l_new_path = os.path.abspath(p_new_path)

		if not l_old_path.startswith(self.m_master_path):
			logging.error("File isn't inside project root: " + l_old_path)
			return False

		if not l_new_path.startswith(self.m_master_path):
			logging.error("File isn't inside project root: " + l_new_path)
			return False

		if not os.path.exists(l_old_path):
			logging.error("File doesn't exists: ", l_old_path)
			return False

		if os.path.exists(l_new_path):
			logging.error("File already exists: ", l_new_path)
			return False

		#TODO: write action

		return False


#==========================================================================
# End
#==========================================================================
