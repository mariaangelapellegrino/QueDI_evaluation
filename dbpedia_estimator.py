import json

#dataset_source = "qald-7-train-en-wikidata.json"
dataset_source = "qald-9-test-multilingual.json"

with open(dataset_source, encoding = "utf-8") as json_file:
	dataset = json.load(json_file)

questions = dataset["questions"]
correct_answers_dict = {}
correct_answers_set = set()
keys = ["uri", "date", "total", "num", "s", "val", "height", "count" , "literal", "c", "string"] 
for question in questions:
	question_id = question["id"]
	correct_answers = question["answers"][0]

	if "bindings" in correct_answers["results"]:
		correct_answers = correct_answers["results"]["bindings"]

		correct_answers_set = set()
		
		for correct_answer in correct_answers:
			found = False
			for key in keys:
				if key in correct_answer:
					found = True
					correct_answers_set.add(correct_answer[key]["value"])
				
			if not found:
				exit(correct_answer)
					
	elif "boolean" in correct_answers:
		correct_answers = correct_answers["boolean"]
	
	else:
		print(correct_answers)
		correct_answers = None
	
		correct_answers_set = set([correct_answers])
	correct_answers_dict[question_id] = correct_answers_set


#dataset_source = "wikidata_skill_replies.json"
dataset_source = "QueDI_QALD9.json"

with open(dataset_source, encoding = "utf-8") as json_file:
	dataset = json.load(json_file)

questions = dataset["questions"]
anwsers_dict = {}
answers_set = set()

for question in questions:
	question_id = question["id"]
	answers = question["answers"][0]

	if "bindings" in answers["results"]:
		answers = answers["results"]["bindings"]

		answers_set = set()
		for answer in answers:
			found = False
			for key in keys:
				if key in answer:
					found = True
					answers_set.add(answer[key]["value"])

			if not found:
				exit(answer)

	elif "boolean" in answers:
		answers = answers["boolean"]
		answers_set = set([answers])

	else: 
		answers_set = set()

	anwsers_dict[question_id] = answers_set

macro_results = {}

total_precision = 0
total_recall = 0
total_f_measure = 0

mean_macro_results = {}

micro_results = {}

all_correct_answers = set()
all_answers = set()

for key in correct_answers_dict:
	correct_answers_set = correct_answers_dict[key]
	if key not in anwsers_dict:
		answers_set = set()
	else:
		answers_set = anwsers_dict[key]

	all_correct_answers = all_correct_answers.union(correct_answers_set)
	all_answers = all_answers.union(answers_set)

	insersect_set = correct_answers_set.intersection(answers_set)

	if len(correct_answers_set) == 0 and len(answers_set) == 0:
		precision = 1
		recall = 1
		f_measure = 1
	elif len(correct_answers_set) == 0 and len(answers_set) > 0:
		precision = 0
		recall = 0
		f_measure = 0
	elif len(correct_answers_set) > 0 and len(answers_set) == 0:
		precision = 0
		recall = 0
		f_measure = 0
	else:
		precision = len(insersect_set) / len(answers_set)
		recall = len(insersect_set) / len(correct_answers_set)

		if (precision+recall)==0:
			f_measure = 0
		else:
			f_measure = 2*(precision*recall)/(precision+recall)
	

	macro_results[key] = {
		'precision' : precision,
		'recall' : recall,
		'f_measure' : recall
	}

	total_precision += precision
	total_recall += recall
	total_f_measure += f_measure

insersect_set = all_correct_answers.intersection(all_answers)

precision = len(insersect_set) / len(all_answers)
recall = len(insersect_set) / len(all_correct_answers)
f_measure = 2*(precision*recall)/(precision+recall)

micro_results = {
	'precision' : precision,
	'recall' : recall,
	'f_measure' : f_measure
}

print("micro results")
print(micro_results)

print("macro results")
num_questions = len(correct_answers_dict)
print(num_questions)
mean_macro_results = {
	'precision' : total_precision/num_questions,
	'recall' : total_recall/num_questions,
	'f_measure' : total_f_measure/num_questions,
}
print(mean_macro_results)





