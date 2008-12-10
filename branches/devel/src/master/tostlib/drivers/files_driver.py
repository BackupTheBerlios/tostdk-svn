#==========================================================================
# tostdk :: tostlib :: drivers :: files_driver.py
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


#==========================================================================
class FilesDriver:
#==========================================================================

	#----------------------------------------------------------------------
	def __init__ ( self, p_configuration ):
	#----------------------------------------------------------------------

		self.m_input_path  = p_configuration.get_option_value('drivers', 'files_driver.input')
		self.m_output_path = p_configuration.get_option_value('drivers', 'files_driver.output')

		self.m_input_handle  = None
		self.m_output_handle = None

	#----------------------------------------------------------------------
	def __del__ ( self ):
	#----------------------------------------------------------------------

		self.close()

	#----------------------------------------------------------------------
	def open ( self, l_configuration ):
	#----------------------------------------------------------------------

		if not self.m_input_path or not self.m_output_path:
			return False

		if not os.path.exists(self.m_input_path):
			try:
				open(self.m_input_path, 'wb').close()
			except:
				return False

		if not os.path.exists(self.m_output_path):
			try:
				open(self.m_output_path, 'wb').close()
			except:
				return False

		try:
			self.m_input_handle  = open(self.m_input_path,  'rb', 0)
			self.m_output_handle = open(self.m_output_path, 'wb', 0)
		except:
			return False

		return True

	#----------------------------------------------------------------------
	def close ( self ):
	#----------------------------------------------------------------------

		l_ret = True

		if self.m_input_handle != None:
			try:
				self.m_input_handle.close()
			except:
				l_ret = False

		if self.m_output_handle != None:
			try:
				self.m_output_handle.close()
			except:
				l_ret = False

		self.m_input_handle  = None
		self.m_output_handle = None

		if os.path.exists(self.m_input_path):
			try:
				os.remove(self.m_input_path)
			except:
				l_ret = False

		if os.path.exists(self.m_output_path):
			try:
				os.remove(self.m_output_path)
			except:
				l_ret = False

		return l_ret

	#----------------------------------------------------------------------
	def read ( self ):
	#----------------------------------------------------------------------

		try:
			l_data = self.m_input_handle.read()
		except:
			l_data = None

		return l_data

	#----------------------------------------------------------------------
	def write ( self, p_data ):
	#----------------------------------------------------------------------

		try:
			self.m_output_handle.write(p_data)
		except:
			return False

		return True


#==========================================================================
# End
#==========================================================================
