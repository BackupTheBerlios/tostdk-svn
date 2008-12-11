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


import packet


#==========================================================================
# Virtual base drivers
#==========================================================================


#==========================================================================
class BaseReadDriver:
#==========================================================================

	#----------------------------------------------------------------------
	def open ( self ):
	#----------------------------------------------------------------------

		raise NotImplementedError

	#----------------------------------------------------------------------
	def close ( self ):
	#----------------------------------------------------------------------

		raise NotImplementedError

	#----------------------------------------------------------------------
	def can_read  ( self ):
	#----------------------------------------------------------------------

		raise NotImplementedError

	#----------------------------------------------------------------------
	def read_byte ( self ):
	#----------------------------------------------------------------------

		raise NotImplementedError


#==========================================================================
class BaseWriteDriver:
#==========================================================================

	#----------------------------------------------------------------------
	def open ( self ):
	#----------------------------------------------------------------------

		raise NotImplementedError

	#----------------------------------------------------------------------
	def close ( self ):
	#----------------------------------------------------------------------

		raise NotImplementedError

	#----------------------------------------------------------------------
	def can_write ( self ):
	#----------------------------------------------------------------------

		raise NotImplementedError

	#----------------------------------------------------------------------
	def write_byte ( self, p_byte ):
	#----------------------------------------------------------------------

		raise NotImplementedError


#==========================================================================
# Buffered base drivers
#==========================================================================


#==========================================================================
class BufferedReadDriver:
#==========================================================================

	#----------------------------------------------------------------------
	def __init__ ( self ):
	#----------------------------------------------------------------------

		self.m_read_handle = None
		self.m_read_buffer = None

	#----------------------------------------------------------------------
	def open ( self, p_handle ):
	#----------------------------------------------------------------------

		self.m_read_handle = p_handle
		self.m_read_buffer = ''

	#----------------------------------------------------------------------
	def close ( self ):
	#----------------------------------------------------------------------

		self.m_read_handle = None
		self.m_read_buffer = None

	#----------------------------------------------------------------------
	def can_read  ( self ):
	#----------------------------------------------------------------------

		try:
			l_read = self.m_read_handle.read()
		except:
			l_read = ''

		self.m_read_buffer += l_read

		return packet.is_valid(self.m_read_buffer)

	#----------------------------------------------------------------------
	def read_byte ( self ):
	#----------------------------------------------------------------------

		if self.m_read_buffer:
			l_byte = self.m_read_buffer[0]
			self.m_read_buffer = self.m_read_buffer[1:]
			return l_byte

		return None


#==========================================================================
class BufferedWriteDriver:
#==========================================================================

	#----------------------------------------------------------------------
	def __init__ ( self ):
	#----------------------------------------------------------------------

		self.m_write_handle = None
		self.m_write_buffer = None

	#----------------------------------------------------------------------
	def open ( self, p_handle ):
	#----------------------------------------------------------------------

		self.m_write_handle = p_handle
		self.m_write_buffer = ''

	#----------------------------------------------------------------------
	def close ( self ):
	#----------------------------------------------------------------------

		self.m_write_handle = None
		self.m_write_buffer = None

	#----------------------------------------------------------------------
	def can_write ( self ):
	#----------------------------------------------------------------------

		return not packet.is_valid(self.m_write_buffer)

	#----------------------------------------------------------------------
	def write_byte ( self, p_byte ):
	#----------------------------------------------------------------------

		self.m_write_buffer += p_byte

		if packet.is_valid(self.m_write_buffer):
			try:
				self.m_write_handle.write(self.m_write_buffer)
			except:
				return False

			self.m_write_buffer = ''

		return True


#==========================================================================
# End
#==========================================================================
