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

from base_driver import BaseDriver


#==========================================================================
class PipesDriver ( BaseDriver ):
#==========================================================================

	#----------------------------------------------------------------------
	def __init__ ( self, p_config ):
	#----------------------------------------------------------------------

		BaseDriver.__init__(self, p_config)

		self.m_command = p_config.get_option_value('drivers', 'pipes_driver.command')
		self.m_popen   = None

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

		return BaseDriver.open(self, self.m_popen.stdout, self.m_popen.stdin)

	#----------------------------------------------------------------------
	def close ( self ):
	#----------------------------------------------------------------------

		l_ret = BaseDriver.close(self)

		if self.m_popen:
			try:
				self.m_popen.wait()
			except:
				l_ret = False

		self.m_popen = None

		return l_ret


#==========================================================================
# End
#==========================================================================
