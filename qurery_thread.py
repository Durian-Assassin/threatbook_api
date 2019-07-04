# -*- coding: UTF-8 -*-
import os
import json
import time
import threading
import sys

"""
read domain list from file
file example:
domain 1
domain 2
...
domain n
"""
# file path
file_path = os.path.abspath('.') + "\domain.txt"
# define the list 0f domain
domain_list = []

try:
	domain_list_file = open(file_path, encoding='UTF-8')
	# the lines of file
	# print(sys.argv[0], "has", len(domain_list_file.readlines()), "lines")

	while True:
		text_line = domain_list_file.readline()
		if text_line:
			domain_list.append(text_line)
		else:
			domain_list_file.close()
			break

except IOError:
	print("cannot open", file_path)

finally:
	print("-----------domain_list len is:", len(domain_list))


def tb_api_query(domain_name, out_file_name):
	try:
		# raw data, return by pipe
		api_call_output = os.popen("python2 domainQuery.py " + domain_name)
		api_call = api_call_output.read()

		# decoding by json.loads
		api_call_json = json.loads(api_call)
		# get the response_code in return json data
		response_code = api_call_json["response_code"]
	except:
		pass

	if response_code == 0:
		try:
			whois_json = api_call_json["cur_whois"]
			out_simple_file = open(os.path.abspath('.') + '\\' + out_file_name + '.txt', 'a', encoding='utf8')

			# simple data
			simple_data = '域名：' + domain_name.strip('\n').strip() + '  注册者：' + whois_json["registrant_name"] + ' \
			电话：' + whois_json["registrant_phone"]
			# write data
			out_simple_file.write(simple_data + "\n")

			out_raw_file = open(os.path.abspath('.') + '\\' + out_file_name + '-raw.txt', 'a', encoding='utf8')
			out_raw_file.write(api_call)
		except IOError as io_err:
			pass

	else:
		try:
			out_raw_file = open(os.path.abspath('.') + '\\' + out_file_name + '-raw.txt', 'a', encoding='utf8')
			out_raw_file.write(api_call)
		except:
			pass


class ApiThread(threading.Thread):

	def __init__(self, thread_id, name, domain_name, out_file_name):
		threading.Thread.__init__(self)
		self.threadID = thread_id
		self.name = name
		self.domain = domain_name
		self.out_file_name = out_file_name

	def run(self):
		print(self.threadID, ":开始查询域名：", self.domain)
		tb_api_query(self.domain, self.out_file_name)
		time.sleep(2)
		print(self.threadID, "查询完成！")


def main():
	try:
		out_file_name = input("Please enter output file name:")
		if "".__eq__(out_file_name):
			os._exit(0)
	except:
		os._exit(0)

	try:
		# 创建新线程
		i = 0
		m = 0  # the start of list
		n = 10  # the end of list

		c = 1  # counter

		for i in range(0, len(domain_list)//10 + 1):
			for x in range(len(domain_list[m:n])):
				thread_list = domain_list[m:n]
				# print("************************", x)
				x = ApiThread(c, repr(c), thread_list[x], out_file_name)
				x.start()
				c += 1

			i += 1
			m = 10 * i + 1
			n = 11 + 10 * i
			time.sleep(2)

	except RuntimeError as run_err:
		print("run time error is:", run_err)


if __name__ == '__main__':
	# start time
	ticks_start = time.time()

	main()
	
	time.sleep(10)

	# end time
	ticks_end = time.time()
	print('start time is:', time.asctime(time.localtime(ticks_start)))
	print('end time is:', time.asctime(time.localtime(ticks_end)))

	time_run = ticks_end - ticks_start
	print('{} {}'.format('run time is ', time_run))

