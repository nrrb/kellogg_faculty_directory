import csv
import datetime
import json
import logging
import os
import time
from urlparse import urljoin
from bs4 import BeautifulSoup
import requests

logging.basicConfig(level=logging.INFO)

def get_faculty_netids():
    response = requests.get("http://www.kellogg.northwestern.edu/faculty/advanced_search.aspx")
    soup = BeautifulSoup(response.content, "lxml")
    return sorted([option['value'] for option in soup.find(id="plcprimarymaincontent_1_selBrowseByName").find_all("option") if option['value']])
        
def get_faculty_info_by_netid(netid):
    def _save_results_to_file(content, filename):
        date_string = datetime.datetime.now().strftime('%Y%m%d')
        save_folder = 'html/' + date_string
        if not os.path.isdir(save_folder):
            os.makedirs(save_folder)
        save_path = save_folder + '/' + filename
        logging.info("Saving content to {0}...".format(save_path))
        with open(save_path, 'wb') as f:
            f.write(content)

    def _get_headshot_image_url(soup):
        # Rough dimensions of headshot image: 166x202
        headshot_image_tag = soup.find(id='imgFacultyImage')
        return urljoin(BASE_URL, headshot_image_tag['src']) if headshot_image_tag else ''

    def _get_faculty_name(soup):
        faculty_name = soup.find(id="lblName").string if soup.find(id="lblName") else ''
        if not faculty_name and soup.find(id='breadCrumbs'):
        # Let's try to get the name from the breadcrumbs text
            faculty_name = list(soup.find(id='breadCrumbs').strings)[-1].strip()
        return faculty_name

    def _get_personal_site(soup):
        sidenav_links = soup.find('div', id='sideNav3').find_all('a')
        personal_site = ''
        for link in sidenav_links:
            if link.text == 'Visit Personal Site':
                personal_site = link.get('href')
        return personal_site

    def _get_office_number(soup):
        return soup.find(id="lblOffice").string if soup.find(id="lblOffice") else ''

    def _get_department(soup):
        return soup.find(id="lblDepartment").string if soup.find(id="lblDepartment") else ''

    def _get_title(soup):
        return soup.find(id="lblTitle").string if soup.find(id="lblTitle") else ''

    def _get_phone(soup):
        return soup.find(id="lblPhone").string if soup.find(id="lblPhone") else ''

    BASE_URL = "http://www.kellogg.northwestern.edu/"
    request_url = "http://www.kellogg.northwestern.edu/faculty/faculty_search_results.aspx?netid={0}".format(netid)
    response = requests.get(request_url)
    html = response.content
    _save_results_to_file(html, response.url.split('/')[-1] + '.html')
    soup = BeautifulSoup(html, "lxml")
    return {'headshot_image_url': _get_headshot_image_url(soup),
            'name': _get_faculty_name(soup),
            'url': response.url,
            'personal_site': _get_personal_site(soup),
            'office': _get_office_number(soup),
            'department': _get_department(soup),
            'title': _get_title(soup),
            'phone': _get_phone(soup)}

def save_dict_list_to_csv(dict_list, filename):
    import csv
    with open(filename, 'wb') as f:
        dw = csv.DictWriter(f, fieldnames=dict_list[0].keys())
        dw.writeheader()
        dw.writerows(dict_list)

if __name__=="__main__":
    netids = get_faculty_netids()
    netid_count = len(netids)
    logging.info("Found {0} Faculty NetIDs.".format(netid_count))

    info_by_netid = {}
    for i, netid in enumerate(netids):
        if netid in info_by_netid:
            logging.info("[{0} of {1}] Already have info for NetID {2}".format(i, netid_count, netid))
        else:
            logging.info("[{0} of {1}] Getting info for NetID {2}".format(i, netid_count, netid))
            info_by_netid[netid] = get_faculty_info_by_netid(netid)

    # Add in netid to the information we've collected
    faculty = []
    for netid, info in info_by_netid.iteritems():
        faculty.append(info)
        faculty[-1]['netid'] = netid

    faculty = sorted(faculty, key=lambda f: f['name'])

    logging.info("Saving data to CSV file...")
    save_dict_list_to_csv(faculty, "faculty.csv")

    logging.info("Saving data to faculty.json...")
    with open('faculty.json', 'w') as f:
        json.dump(faculty, f)

    logging.info("Saving data (with names) to faculty_with_names.json...")
    with open('faculty_with_names.json', 'w') as f:
        faculty_with_names = filter(lambda f: f['name'], faculty)
        json.dump(faculty_with_names, f)

    logging.info("Saving data (with names and faces) to faculty_with_names_and_faces.json...")
    with open('faculty_with_names_and_faces.json', 'w') as f:
        faculty_with_names_and_faces = filter(lambda f: f['name'] and f['headshot_image_url'], faculty)
        json.dump(faculty_with_names_and_faces, f)
