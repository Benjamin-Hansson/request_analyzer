from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.chrome.options import Options
import sys
import json
from file_handling import *
import time


url_start = "http://www."

def main(file_name, number):
	print("Running through urls in", file_name)
	urls = []
	# loads all domains into urls
	index = 0
	low = (number)*5000
	high = (number+1) * 5000
	with open(file_name, "r") as file:
		line = file.readline()
		while line and index < high:
			if low <= index:
				url = url_start + line[line.index(',')+1:]
				if url[-1] == "\n":
					url = url[:-1]
				urls.append(url)

			index += 1
			line = file.readline()

	get_requests(urls, number)

def create_tracker_list(disconnect):
	lst = []
	for domain in disconnect:
		lst += disconnect[domain]["properties"]
		lst += disconnect[domain]["resources"]

	lst = [url_magic(elem) for elem in lst]
	val = set(lst)
	return val

# Counts external requests
def get_requests(urls, number):
	st_t = time.time()
	domains = read_data_file(number)

	file = open('disconnect_list.json', 'r')
	disconnect_list = create_tracker_list(json.loads(file.read()))
	#print(disconnect_list)
	counter = 0
	for url in urls:
		if url_magic(url) in domains:
			continue
		options = Options()
		options.add_argument("--headless")
		try:
			driver = webdriver.Chrome(chrome_options=options, seleniumwire_options={'verify_ssl': False})
		except Exception as e:
			print("error:", e)
			continue
		start_time = time.time()
		#print("Analyzing", url ,"-------------------------")
		driver.delete_all_cookies()
		org_domain = url_magic(url)

		try:
			#print("Making request to", url)
			driver.get(url)
		except Exception as e:

			print("error: ", e)
			driver.quit()
			continue
		#print("Response recieved, ammount of requests:", len(driver.requests))


		domains[org_domain] = {"externalRequests": {}, "knownTrackers":{}}
		try:
			for request in driver.requests:
				domain = url_magic(request.path)
				if request.response and domain not in url:
					if domain in domains[org_domain]["externalRequests"]:
						domains[org_domain]["externalRequests"][domain] += 1
					else:
						domains[org_domain]["externalRequests"][domain] = 1
					if requests_in_know_trackers(domain, disconnect_list):
						if domain in domains[org_domain]["knownTrackers"]:
							domains[org_domain]["knownTrackers"][domain] += 1
						else:
							domains[org_domain]["knownTrackers"][domain] = 1
		except Exception as e:
			driver.quit()
			continue
		#print("Done in", time.time()-start_time, "seconds")
		driver.quit()
		counter += 1
		if counter % 10 == 0:
			write_data_file(domains, number)
			print("process number {} saved".format(number))
	write_data_file(domains, number)
	print("Analyzed {} urls in {} seconds".format(len(urls), time.time()-st_t))
	return domains


def requests_in_know_trackers(externalReq, disconnect_list):
	known_trackers = {}

	return externalReq in disconnect_list


# Extracts domain from url
def url_magic(url):
	# Remove http://
	cut = url.find('://')
	if (cut != -1):
		no_http = url[cut + 3:]
	else:
		no_http = url

	#print("Url utan http:// : ", no_http)

	# Remove object path from url
	domain = no_http.find('/')
	if (domain != -1):
		webserver = no_http[:domain]
	else:
		webserver = no_http

	'''
	port_pos = webserver.find(":")
	if (port_pos != -1):
		webserver = webserver[:port_pos]
	'''

	# Ta bort .se, .com etc.
	cut_prefix = webserver.rfind(".")
	if (cut_prefix != -1):
		webserver = webserver[:cut_prefix]

	# Ta bort www eller motsvarig
	cut_prefix = webserver.rfind(".")
	if (cut_prefix != -1):
		webserver = webserver[cut_prefix + 1:]

	#print("webserver: ", webserver)
	return webserver


if __name__ == '__main__':
	number = int(sys.argv[1])
	main("request_lists/top-100k.csv", number)