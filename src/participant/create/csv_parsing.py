


def csv_parse(file):
	ret = []
	first_line = ""

	for elem in file:

		sub_ret = {}
		elem = elem.decode("utf-8")
		elem = elem.replace("\n","")
		elem = elem.replace("\r","")
		elem = elem.replace(";",",")
		elem = elem.split(",")
		
		if first_line == "":
			# first_line = elem.split(",")
			first_line = elem
			continue

		print(first_line)

		try:
			if first_line.count("email")>0: sub_ret["email"] = elem[first_line.index("email")]
			if first_line.count("first_name")>0: sub_ret["first_name"] = elem[first_line.index("first_name")]
			if first_line.count("last_name")>0: sub_ret["last_name"] = elem[first_line.index("last_name")]
			if first_line.count("division")>0: sub_ret["division"] = elem[first_line.index("division")]
			if first_line.count("division_leader")>0: sub_ret["division_leader"] = elem[first_line.index("division_leader")]
			if first_line.count("is_vip")>0: sub_ret["is_vip"] = elem[first_line.index("is_vip")]
		except:
			continue


		if sub_ret.get("is_vip") == "true"\
			or sub_ret.get("is_vip") == "True"\
			or sub_ret.get("is_vip") == "1" : 
			sub_ret["is_vip"] = True
		else:
			sub_ret["is_vip"] = False

		ret.append(sub_ret)
	print(first_line)
	print(ret)
	return ret

