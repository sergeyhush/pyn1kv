import pexpect

class VsmPexpect(object):

	def __init__(self):
		self.connection = None
		self.end_output = None
		self.no_pagination = True

	def connect(self, vsm_ip, username, password):
		self.connection = pexpect.spawn('ssh {1}@{0}'.format(vsm_ip,username))
		try:
			self.connection.expect('.*assword:*')
			self.connection.sendline(password)
			self.connection.expect('#')
		except:
			print "Could not connect to {0}:\n {1}".format(vsm_ip, str(self.connection))
		if  self.end_output is None:
			self.__try_get_end_output_pattern()

	def __try_get_end_output_pattern(self):
		expect_char = '#'
		if self.connection:
			self.connection.sendline(' ')
			self.connection.expect(expect_char)
			self.end_output = self.connection.before.strip() + expect_char

	def disconnect(self):
		if self.connection:
			self.connection.sendline('exit')

	def _strip_terminal_output(self,str):
		str = str.strip()
		i = str.find('\n')
		if i == -1: 
			return ' '
		else:
			return str[i + 1:]


	def raw_command(self, cmd, expect):
		try:
			print "EXEC <{0}> EXPECT <{1}>".format(cmd,expect)
			self.connection.sendline(cmd)
			self.connection.expect(expect)
			return self._strip_terminal_output(self.connection.before)
		except:
			print "Could not execute <{0}>\n {1}".format(cmd, str(self.connection))

	def show(self, cmd):
		show_cmd = cmd + " | no-more"
		return self.raw_command(show_cmd, self.end_output)


	def configure(self, conf_cmds):
		expect = self.end_output[:-1] + '\(confi.*\)' + self.end_output[-1]
		cmds = []
		if isinstance(conf_cmds, str):
			cmds = conf_cmds.split(',')
		elif isinstance(conf_cmds, list):
			cmds = conf_cmds
		else:
			raise TypeError('Commands must be a list of a CSV string')

		self.raw_command('configure terminal', '#')
		for i in cmds:
			self.raw_command(i.strip(), expect)
		self.raw_command('end', self.end_output)



if __name__ == '__main__':
	vsm = "172.23.233.65"
	username = "admin"
	password = "Sfish123"
	p = VsmPexpect()
	p.connect(vsm, username, password)
   	print p.show('show clock')
   	p.configure(['network-segment test_ns1', 'network-definition test_nd1','switchport access vlan 301'])

	p.disconnect()