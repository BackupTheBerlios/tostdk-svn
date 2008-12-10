#==========================================================================
# tostdk :: tostlib :: drivers :: pipes_driver.py
# Driver using piped command
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


import subprocess


#==========================================================================
class PipesDriver:
#==========================================================================

	#----------------------------------------------------------------------
	def __init__ ( self, p_configuration ):
	#----------------------------------------------------------------------

		self.m_command = p_configuration.get_option_value('drivers', 'pipes_driver.command')
		self.m_popen   = None

	#----------------------------------------------------------------------
	def __del__ ( self ):
	#----------------------------------------------------------------------

		self.close()

	#----------------------------------------------------------------------
	def open ( self ):
	#----------------------------------------------------------------------

		if not self.m_command:
			return False

		try:
			self.m_popen = subprocess.Popen(self.m_command, bufsize=0,
											stdin=subprocess.PIPE,
											stdout=subprocess.PIPE,
											close_fds=True)
		except:
			self.m_popen = None
			return False

		return True

	#----------------------------------------------------------------------
	def close ( self ):
	#----------------------------------------------------------------------

		l_ret = True

		if self.m_popen:
			try:
				self.m_popen.wait()
			except:
				l_ret = False

		self.m_popen = None

		return l_ret

	#----------------------------------------------------------------------
	def can_read  ( self ): return (self.m_popen.pool() == None)
	def can_write ( self ): return (self.m_popen.pool() == None)
	#----------------------------------------------------------------------

	#----------------------------------------------------------------------
	def read_byte ( self ):
	#----------------------------------------------------------------------

		try:
			l_byte = self.m_popen.stdout.read(1)
		except:
			l_byte = None

		return l_byte

	#----------------------------------------------------------------------
	def write_byte ( self, p_byte ):
	#----------------------------------------------------------------------

		try:
			self.m_popen.stdin.write(p_byte)
		except:
			return False

		return True


#==========================================================================
# End
#==========================================================================
