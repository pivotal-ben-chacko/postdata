import xml.etree.ElementTree as ET

import os
import json
import datetime
# import requests

def format_time():
    time = datetime.datetime.now()
    formatted_time = time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    return formatted_time[:-5] + 'Z'

def main():

    url = 'https://gating.cvshealth.com/api/v1/build'
    headers = {'Content-type': 'application/json', 'accept': '*/*'}

    project_name = os.path.basename(os.getcwd())

    total_unit_tests = 0
    total_unit_test_failures = 0
    total_unit_test_success = 0

    total_bdd_tests = 0
    total_bdd_failures = 0
    total_bdd_success = 0

    try:

        unit_tree = ET.parse('unit-test-results.xml')
        unit_root = unit_tree.getroot()
        unit_testsuites_attributes = unit_root.attrib

        total_unit_tests = int(unit_testsuites_attributes['tests'])
        total_unit_test_failures = int(unit_testsuites_attributes['failures'])
        total_unit_test_success = total_unit_tests - total_unit_test_failures

        bdd_tree = ET.parse('bdd-test-results.xml')
        bdd_root = bdd_tree.getroot()
        bdd_testsuites_attributes = bdd_root.attrib

        total_bdd_tests = int(bdd_testsuites_attributes['tests'])
        total_bdd_failures = int(bdd_testsuites_attributes['failures'])
        total_bdd_success = total_bdd_tests - total_bdd_failures

    except:
        print("Unable to find the file")

    build_result = 'Failure' if ( total_bdd_failures != 0 or total_unit_test_failures != 0 ) else 'Success'

    data = {}
    data['projectName'] = project_name
    data['buildNumber'] = 'TODO: way to increment the build Number'
    data['buildTime'] = format_time()
    data['buildResult'] = build_result
    data['testsExecuted'] = total_unit_tests
    data['testsPassed'] = total_unit_test_success
    data['scenarios'] = total_bdd_tests
    data['scenariosCovered'] = total_bdd_success
    data['scenariosNotCovered'] = total_bdd_failures
    data['scenariosPassed'] = total_bdd_success
    data['scenariosFailed'] = total_bdd_failures
    data['ciTool'] = 'SupplyChain'
    data['jobName'] = project_name
    data['sourceUrl'] = 'TODO: get full path of supply chain'

    json_data = json.dumps(data)
    # session = requests.Session()
    print(json_data)
    print(headers)
    print(url)

    # res = requests.post(url, data=json_data, headers=headers)
    # print("Status code: " + str(res.status_code))
    # print(res.text)

if __name__ == '__main__':
    main()
