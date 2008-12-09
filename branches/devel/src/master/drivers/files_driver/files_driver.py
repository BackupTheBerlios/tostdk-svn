#==========================================================================
# tostdk :: drivers :: files_driver.py
# Test driver, using files for input / output
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

import drivers.driver as driver
import tostlib.configuration as configuration

#==========================================================================
class FilesDriver ( driver.Driver ):
#==========================================================================

	#----------------------------------------------------------------------
	def __init__ ( self ):
	#----------------------------------------------------------------------

		driver.Driver.__init__(self)

		self.m_input_handle  = None
		self.m_output_handle = None

	#----------------------------------------------------------------------
	def open ( self ):
	#----------------------------------------------------------------------

		l_config = configuration.Configuration.get_instance()

		l_input_path  = l_config.get_option_value('drivers', 'files_driver.input')
		l_output_path = l_config.get_option_value('drivers', 'files_driver.output')

		if not l_input_path or not l_output_path:
			return False

		try:
			open(l_input_path,  'wb').close()
			open(l_output_path, 'wb').close()
		except:
			return False

		self.m_input_handle  = open(l_input_path,  'rb', 0)
		self.m_output_handle = open(l_output_path, 'wb', 0)

		return True

	#----------------------------------------------------------------------
	def close ( self ):
	#----------------------------------------------------------------------

		if self.m_input_handle != None:
			self.m_input_handle.close()

		if self.m_output_handle != None:
			self.m_output_handle.close()

	#----------------------------------------------------------------------
	def read ( self ):
	#----------------------------------------------------------------------

		return self.m_input_handle.read()

	#----------------------------------------------------------------------
	def write ( self, p_data ):
	#----------------------------------------------------------------------

		self.m_output_handle.write(p_data)


#==========================================================================
# End
#==========================================================================
