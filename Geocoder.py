## UPRN Geocoder Script ##

## import python library
import csv, json, requests

## Read csv of UPRNs
def import_uprn():
	with open('uprn_targets.csv') as import_csv:
		reader = csv.reader(import_csv)
		import_list = list(reader)
		uprn_targets = []
		uprn_targets.extend(import_list)
	return uprn_targets

## http GET each UPRN
def query_SDS_api(uprn):
	params = {
		"format":"all", 
		"query":"all", 
		"uprn":uprn
	}
	url = 'https://address.digitalservices.surreyi.gov.uk/addresses'
	headers = {"Authorization":"Bearer my_secret_api_key"}
	r = requests.get(url,params=params,headers=headers)
	if len(r.json()) == 0:
		print(uprn + ' not found')
	elif len(r.json()) > 0:
		parse_json_response(r)
		return r

## parse json data
def parse_json_response(r):
	json_parsed = json.loads(json.dumps(r.json()))
	uprn = json_parsed[0]['uprn']
	easting = json_parsed[0]['location']['easting']
	northing = json_parsed[0]['location']['northing']
	append_result_to_csv(uprn, easting, northing)

## append to csv
def append_result_to_csv(uprn, easting, northing):
	with open('uprn_geocoded.csv', 'a') as outcsv:
		writer = csv.writer(outcsv, delimiter=',', lineterminator='\n')
		writer.writerow([uprn, easting, northing])
		print(uprn + ' appended to csv')

## Run the geocoder
def Geocode():
	uprn_targets_tuple = import_uprn()
	uprn_targets = [i for sub in uprn_targets_tuple for i in sub]
	for uprn in uprn_targets:
		query_SDS_api(uprn)
	
Geocode()