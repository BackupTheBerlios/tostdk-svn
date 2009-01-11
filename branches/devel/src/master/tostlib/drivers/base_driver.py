#==========================================================================
# tostdk :: tostlib :: drivers :: base_driver.py
# Base driver class
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


#==========================================================================
class BaseDriver:
#==========================================================================

	#----------------------------------------------------------------------
	def __init__ ( self, p_config ):
	#----------------------------------------------------------------------

		self.m_read_handle  = None
		self.m_write_handle = None

	#----------------------------------------------------------------------
	def open ( self, p_read_handle, p_write_handle ):
	#----------------------------------------------------------------------

		self.m_read_handle  = p_read_handle
		self.m_write_handle = p_write_handle

		return True

	#----------------------------------------------------------------------
	def close ( self ):
	#----------------------------------------------------------------------

		self.m_read_handle  = None
		self.m_write_handle = None

		return True

	#----------------------------------------------------------------------
	def read ( self ):
	#----------------------------------------------------------------------

		try:
			l_data = self.m_read_handle.read()
		except:
			l_data = ''

		return l_data

	#----------------------------------------------------------------------
	def write ( self, p_data ):
	#----------------------------------------------------------------------

		try:
			self.m_write_handle.write(p_data)
		except:
			return False

		return True


#==========================================================================
# End
#==========================================================================
