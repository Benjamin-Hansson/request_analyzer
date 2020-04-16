import sys
import json
import csv

savefile = "collected_data/final.json"

csv_file = "collected_data/test.csv"

g_fb_a_file = "collected_data/g_fb_a.csv"


def main():
	data = {}
	with open(savefile, "r") as file:
		data = json.loads(file.read())
	print("total responses out of 100k:", get_domain_count(data))
	print("average ammount of requests to known trackers:", get_average_tracker_ammount(data))

	print("------")
	print("average ammount of different trackers:", get_average_different_trackers(data))

	print("------")
	print("average ammount of external requests:", get_average_external_request_amount(data))

	print("------")
	print("average ammount of external requests to different domains:", get_average_different_external_requests(data))

	print("------")
	print("average ammount of requests to known trackers no 0:", get_average_tracker_ammount_no_0(data))

	print("------")
	print("average ammount of different trackers no 0:", get_average_different_trackers_no_0(data))

	print("------")
	print("average ammount of external requests no 0:", get_average_external_request_amount_no_0(data))

	print("------")
	print("average ammount of external requests to different domains no 0:", get_average_different_external_requests_no_0(data))


	print("------")
	result1 = ammount_to_google_facebook_amazon(data)
	print("average ammount of external requests to google: ", result1[0])
	print("average ammount of external requests to facebook: ", result1[1])
	print("average ammount of external requests to amazon: ", result1[2])
	print("------")
	result2 = unique_ammount_to_google_facebook_amazon(data)
	print("unique domains with google present", result2[0])
	print("unique domains with facebook present", result2[1])
	print("unique domains with amazon present", result2[2])
	# export_g_fb_a(result1, result2)

	print("------")
	print("ammount with no external domains: ", ammount_no_external(data))
	print("ammount with no known trackers: ", ammount_no_known_trackers(data))

	categories1 = divide_data(data, known_trackers=False, unique=True)
	print(categories1)
	categories2 = divide_data(data, known_trackers=True, unique=True)
	print(categories2)
	categories3 = divide_data(data, known_trackers=False, unique=False)
	print(categories3)
	categories4 = divide_data(data, known_trackers=True, unique=False)
	print(categories4)


	'''	
	with open("collected_data/analysis1.csv", newline='', mode='w') as my_file:
		fields = ["amount", "external unique", "known unique", "amount external", "amount unique"]
		writer = csv.DictWriter(my_file, fieldnames=fields)
		writer.writeheader()
		writer.writerow({"amount": '0', "external unique": categories1[0], "known unique": categories2[0],
							"amount external": categories3[0], "amount unique": categories4[0]})
		for i in range(1, 11):
			writer.writerow({"amount": str((i - 1) * 10) + "-" + str(i * 10), "external unique": categories1[i],
								"known unique": categories2[i],
								"amount external": categories3[i], "amount unique": categories4[i]})
		writer.writerow({"amount": "100+", "external unique": categories1[11],
								"known unique": categories2[11],
								"amount external": categories3[11], "amount unique": categories4[11]})
	
	'''




def divide_data(data, known_trackers: bool, unique: bool):
	'''
	divides the data into 11 categories where each category represents the total ammount of requests made
	The devision is into the categories: 0, 1-10 11-20, ..., 91-100, 100+
	:param data:
	:return:
	'''
	string = "knownTrackers" if known_trackers else "externalRequests"
	categories = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	for domain in data:
		requests = data[domain][string]
		amount = 0
		if unique:
			amount = len(data[domain][string])
		else:
			for request in requests:
				amount += requests[request]
		for i in range(1, 11):
			if amount == 0:
				categories[0] += 1
				break
			if (i - 1) * 10 < amount <= i * 10:
				categories[i] += 1
				break
		else:
			categories[11] += 1
	return categories


def export_g_fb_a(average_amount, average_unique):
	with open(g_fb_a_file, newline='', mode='w') as my_file:
		fields = ['domain', 'average_amount', 'average_unique']
		writer = csv.DictWriter(my_file, fieldnames=fields)
		writer.writeheader()
		writer.writerow({'domain': 'google', 'average_amount': average_amount[0], 'average_unique': average_unique[0]})
		writer.writerow(
			{'domain': 'facebook', 'average_amount': average_amount[1], 'average_unique': average_unique[1]})
		writer.writerow({'domain': 'amazon', 'average_amount': average_amount[2], 'average_unique': average_unique[2]})


def export_to_excel(data):
	with open(csv_file, newline='', mode='w') as my_file:
		fields = ['domain', 'external', 'known']
		writer = csv.DictWriter(my_file, fieldnames=fields)
		writer.writeheader()
		for domain in data:
			external_requests = data[domain]["externalRequests"]
			known_trackers = data[domain]["knownTrackers"]
			writer.writerow({'domain': domain, 'external': len(external_requests), 'known': len(known_trackers)})


def ammount_no_external(data):
	total = 0
	for domain in data:
		external_requests = data[domain]["externalRequests"]
		if len(external_requests) == 0:
			total += 1
	return total


def ammount_no_known_trackers(data):
	total = 0
	for domain in data:
		known_trackers = data[domain]["knownTrackers"]
		if len(known_trackers) == 0:
			total += 1
	return total


def get_domain_count(data):
	return len(data)


def get_average_tracker_ammount(data):
	total = 0
	for domain in data:
		known_trackers = data[domain]["knownTrackers"]
		for tracker in known_trackers:
			total += known_trackers[tracker]
	return total / len(data)


def get_average_tracker_ammount_no_0(data):
	total = 0
	amount = 0
	for domain in data:
		known_trackers = data[domain]["knownTrackers"]
		if len(known_trackers) > 0:
			amount += 1
		for tracker in known_trackers:
			total += known_trackers[tracker]
	return total / amount


def get_average_different_trackers(data):
	total = 0

	for domain in data:
		known_trackers = data[domain]["knownTrackers"]
		total += len(known_trackers)
	return total / len(data)


def get_average_different_trackers_no_0(data):
	total = 0
	amount = 0
	for domain in data:
		known_trackers = data[domain]["knownTrackers"]
		if len(known_trackers) > 0:
			amount += 1
		total += len(known_trackers)
	return total / amount


def get_average_external_request_amount(data):
	total = 0
	for domain in data:
		external_requests = data[domain]["externalRequests"]
		for tracker in external_requests:
			total += external_requests[tracker]
	return total / len(data)


def get_average_external_request_amount_no_0(data):
	total = 0
	amount = 0
	for domain in data:
		external_requests = data[domain]["externalRequests"]
		if len(external_requests) > 0:
			amount += 1
		for tracker in external_requests:
			total += external_requests[tracker]
	return total / amount


def get_average_different_external_requests(data):
	total = 0

	for domain in data:
		external_requests = data[domain]["externalRequests"]
		total += len(external_requests)
	return total / len(data)


def get_average_different_external_requests_no_0(data):
	total = 0
	amount = 0
	for domain in data:
		external_requests = data[domain]["externalRequests"]
		if len(external_requests) > 0:
			amount += 1
		total += len(external_requests)
	return total / amount



def ammount_to_google_facebook_amazon(data):
	global google
	global facebook
	global amazon

	g_tot = 0
	fb_tot = 0
	a_tot = 0

	for domain in data:
		external_requests = data[domain]["externalRequests"]
		for external_request in external_requests:
			if external_request in google:
				g_tot += external_requests[external_request]
			if external_request in facebook:
				fb_tot += external_requests[external_request]
			if external_request in amazon:
				a_tot += external_requests[external_request]

	return g_tot / len(data), fb_tot / len(data), a_tot / len(data)


def unique_ammount_to_google_facebook_amazon(data):
	global google
	global facebook
	global amazon

	g_tot = 0
	fb_tot = 0
	a_tot = 0
	for domain in data:
		external_requests = data[domain]["externalRequests"]
		g = False
		fb = False
		a = False

		for external_request in external_requests:
			if external_request in google and not g:
				g_tot += 1
				g = True
			if external_request in facebook and not fb:
				fb_tot += 1
				fb = True
			if external_request in amazon and not a:
				a_tot += 1
				a = True
	return g_tot, fb_tot, a_tot


facebook = [
	"facebook",
	"fb",
	"friendfeed",
	"instagram",
	"fbcdn",
	"messenger",
	"atlassolutions"
	"messenger"
]
amazon = [
	"amazon",
	"assoc-amazon",
	"alexa",
	"amazonaws",
	"amazon",
	"amazon-adsystem",
	"assoc-amazon",
	"alexa",
	"alexametrics",
	"cloudfront",
	"amazonaws"
]
google = [
	"abc",
	"google",
	"ingress",
	"admeld",
	"blogger",
	"google-melange.",
	"google.cat",
	"panoramio",
	"youtube",
	"google",
	"2mdn",
	"admeld",
	"admob",
	"cc-dt",
	"destinationurl",
	"doubleclick",
	"gmail",
	"google-analytics",
	"googleadservices",
	"googlemail",
	"googlesyndication",
	"googlevideo",
	"googletagservices",
	"invitemedia",
	"postrank",
	"smtad",
	"apture",
	"blogger",
	"ggpht",
	"gmodules",
	"googleapis",
	"googleusercontent",
	"gstatic",
	"recaptcha",
	"youtube",
	"googletagmanager"
]

if __name__ == '__main__':
	main()
