


def csv_parse(file):
	ret = []
	first_line = ""


	for elem in file:
		sub_ret = {}
		elem = elem.decode("utf-8")
		elem = elem.replace("\n","")
		elem = elem.split(",")
		
		if first_line == "":
			first_line = file.split(",")
			continue

		if first_line.get("email"): sub_ret["email"] = elem[first_line.index("email")]
		if first_line.get("first_name"): sub_ret["first_name"] = elem[first_line.index("first_name")]
		if first_line.get("last_name"): sub_ret["last_name"] = elem[first_line.index("last_name")]
		if first_line.get("division"): sub_ret["division"] = elem[first_line.index("division")]
		if first_line.get("division_leader"): sub_ret["division_leader"] = elem[first_line.index("division_leader")]
		
		# sub_ret["last_name"] = elem[1]
		# sub_ret["division"] = elem[3]
		# sub_ret["division_leader"] = elem[4]

		ret.append(sub_ret)

	print(f"ret: {ret}")
	return ret