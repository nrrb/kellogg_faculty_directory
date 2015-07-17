import csv
import json
import time
from urlparse import urljoin
from bs4 import BeautifulSoup
import requests


def get_faculty_netids():
    response = requests.get("http://www.kellogg.northwestern.edu/faculty/advanced_search.aspx")
    soup = BeautifulSoup(response.content)
    return sorted([option['value'] for option in soup.find(id="plcprimarymaincontent_1_selBrowseByName").find_all("option") if option['value']])
        
def get_faculty_info_by_netid(netid):
    BASE_URL = "http://www.kellogg.northwestern.edu/"
    response = requests.get("http://www.kellogg.northwestern.edu/faculty/faculty_search_results.aspx?netid={0}".format(netid))
    soup = BeautifulSoup(response.content)
    headshot_image_tag = soup.find(id="imgFacultyImage")
    if headshot_image_tag:
        headshot_image_url = urljoin(BASE_URL, headshot_image_tag['src'])
    else:
        headshot_image_url = ''
    return {'headshot_image_url': headshot_image_url,
            'name': soup.find(id="lblName").string if soup.find(id="lblName") else '',
            'url': response.url,
            'office': soup.find(id="lblOffice").string if soup.find(id="lblOffice") else '',
            'department': soup.find(id="lblDepartment").string if soup.find(id="lblDepartment") else '',
            'title': soup.find(id="lblTitle").string if soup.find(id="lblTitle") else ''}

def save_list_to_csv(dict_list, filename):
    import csv
    with open(filename, 'wb') as f:
        dw = csv.DictWriter(f, fieldnames=dict_list[0].keys())
        dw.writeheader()
        dw.writerows(dict_list)


netids = get_faculty_netids()

info_by_netid = {}
print "Already have info for netids: {0}".format(', '.join(sorted(info_by_netid.keys())))
for netid in netids:
    if netid not in info_by_netid:
        print "Getting info for {0}".format(netid)
        info_by_netid[netid] = get_faculty_info_by_netid(netid)
        time.sleep(0.2)

save_list_to_csv(info_by_netid.values(), "faculty.csv")

with open('faculty.csv', 'r') as f:
	faculty = list(csv.DictReader(f))

faculty_with_names_and_faces = filter(lambda f: f['name'] and f['headshot_image_url'], faculty)

with open('faculty.json', 'w') as f:
	json.dump(faculty_with_names_and_faces, f)