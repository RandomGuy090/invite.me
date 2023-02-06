// Declare a fragment:
var fragment = document.createDocumentFragment();

var events = document.getElementsByClassName("participant")
var eventsList = {}
var divisionList = {}

for (var i = 0; i < events.length; i++) {
	var classes = events[i].classList

	for(elem in classes){

		if(typeof classes[elem] === "string" && elem !== "value"){

			if(classes[elem].startsWith("event_name-")){

				if (typeof eventsList[classes[elem]] === "undefined" && elem !== "value"){
					eventsList[classes[elem]] = Array()
				}
			}

			if(classes[elem].startsWith("division-")){

				for(ev in classes){
					if (typeof classes[ev] === "string" && classes[ev].startsWith("event_name-") && ev !== "value"){
						
						// console.log(`${classes[ev]} (${eventsList[classes[ev]].length}) ---> ${classes[elem]} (${classes[elem]})`)
						if (typeof eventsList[classes[ev]][classes[elem]] === "undefined" && classes[ev] !== "value") {
							eventsList[classes[ev]][classes[elem]] = Array()
						}
						// console.log(`${i} ${events[i]}`)
						eventsList[classes[ev]][classes[elem]].push(events[i])

					}
				}
			}
		}
	}	
}

var participDiv = document.getElementsByClassName("participants")[0]
var newDiv = document.createElement("div")
var summary = document.createElement("div")
// summary.innerHTML = "Events"
newDiv.appendChild(summary)
var fields = ["remove","id","first_name","last_name","email","event","User_email","added by user id", "VIP","Declarated","Division","go to declaration","go to invitation","event_id","send declaration","send invitation ","cancelled"]

for(event in eventsList ){
	
	var summary = document.createElement("summary")
	var event_name = event.split("-")[1]
	event_name = event_name.replaceAll("_", " ")
	summary.innerHTML = `<h3>${event_name}</h3>`
	console.log(event)
	newDiv.appendChild(summary)
	newDiv.appendChild(document.createElement("hr"))

	for (division in eventsList[event]){
		var newDivision = document.createElement("details")
		var sumDiv = document.createElement("summary")
		sumDiv.innerHTML = division.split("-")[1]

		newDivision.appendChild(sumDiv)
		newDiv.appendChild(newDivision)
		
		var headers = document.createElement("tr")
		for(i in fields){
			var x = document.createElement("th")
			x.innerHTML = fields[i]
			headers.appendChild(x)

		}
		newDivision.appendChild(headers)

		for(elem in eventsList[event][division]){
			newDivision.appendChild(eventsList[event][division][elem])
			// console.log(eventsList[event][division][elem])

		}
	}
	
	// newDiv.append(summary)
}
participDiv.appendChild(newDiv)

console.log(newDiv)
console.log(eventsList)



// focus on element

var hash = document.location.hash;
console.log(hash)
console.log(hash)
console.log(hash)

if (hash !== ""){
	hash = hash.substring(1);
	var focusElem = document.getElementById(hash);
	console.log(focusElem)

	focusElem.parentElement.parentElement.open = true
	focusElem.focus()
}