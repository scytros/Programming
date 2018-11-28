import requests
import re

governmentKey = "cc464db4456fe968b76f16c6a84b286dad9a9ac413634751814eaeb9769b6906"  # API key for overheid.io
header = {"ovio-api-key": governmentKey}  # header to get access to the database of overheid.io

alprApi = "sk_25f871e3d65e30b86d749fe3"  # API key for openalpr.com
alprUrl = "https://api.openalpr.com/v2/recognize?secret_key=" + alprApi + "&recognize_vehicle=0&country=eu&state=nl&return_image=0&topn=10"  # URL for openalpr.com to read out the photo's
govUrl = "https://overheid.io/api/voertuiggegevens/"


def get_license(data):
    """"Gets a licence plate from the data"""
    try:
        license = data['results'][0]['plate']
        updated_license = ""
        if (license):
            # check if license matches sidecode 9
            if re.match('[A-Z][A-Z]\d\d\d[A-Z]', license):
                license_list = list(license)
                license_list.insert(2, '-')
                license_list.insert(6, '-')
                updated_license = ''.join(license_list)
            # license plate is not sidecode 9? check if license matches sidecode 8
            elif re.match('\d[A-Z][A-Z][A-Z]\d\d', license):
                license_list = list(license)
                license_list.insert(1, '-')
                license_list.insert(5, '-')
                updated_license = ''.join(license_list)
            # license plate is not sidecode 9 or 8? check if license matches sidecode 7
            elif re.match('\d\d[A-Z][A-Z][A-Z]\d', license):
                license_list = list(license)
                license_list.insert(2, '-')
                license_list.insert(6, '-')
                updated_license = ''.join(license_list)
            # if the plate does not match one of the above fallback to sidecode 4/5/6
            else:
                license_list = list(license)
                license_list.insert(2, '-')
                license_list.insert(5, '-')
                updated_license = ''.join(license_list)

    except IndexError:
        updated_license = ""
    except TypeError:
        updated_license = ""

    return updated_license


def send_plate(plate):
    """"Sends plate to server, and returns the data in json"""
    response_rdw = requests.get(govUrl + plate, headers=header)
    return response_rdw.json()

