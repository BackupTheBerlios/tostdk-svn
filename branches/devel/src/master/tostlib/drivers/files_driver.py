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


from base_driver import BaseDriver


#==========================================================================
class FilesDriver ( BaseDriver ):
#==========================================================================

	#----------------------------------------------------------------------
	def __init__ ( self, p_config ):
	#----------------------------------------------------------------------

		BaseDriver.__init__(self, p_config)

		self.m_input_path  = p_config.get_option_value('drivers', 'files_driver.input')
		self.m_output_path = p_config.get_option_value('drivers', 'files_driver.output')

		self.m_input_handle  = None
		self.m_output_handle = None

	#----------------------------------------------------------------------
	def open ( self ):
	#----------------------------------------------------------------------

		if not self.m_input_path or not self.m_output_path:
			return False

		try:
			self.m_input_handle  = open(self.m_input_path,  'rb', 0)
			self.m_output_handle = open(self.m_output_path, 'wb', 0)

		except:
			self.m_input_handle  = None
			self.m_output_handle = None
			return False

		return BaseDriver.open(self, self.m_input_handle, self.m_output_handle)

	#----------------------------------------------------------------------
	def close ( self ):
	#----------------------------------------------------------------------

		l_ret = BaseDriver.close(self)

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

		return l_ret


#==========================================================================
# End
#==========================================================================
