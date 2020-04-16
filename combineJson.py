import sys
import json

path="collected_data/list"
ending=".json"
savefile="collected_data/final.json"


def combine_json(number):
	lst = []
	for i in range(number):
		print("adding list 1")
		with open(path + str(i) + ending, "r") as file:
			lst.append(json.loads(file.read()))
	data = {}
	for part in lst:
		data.update(part)
	with open(savefile, "w+") as file:
		file.write(json.dumps(data, indent=4))
	print("Total of",len(data),"Domains analyzed")


if __name__ == '__main__':
	number = int(sys.argv[1])

	combine_json(number)