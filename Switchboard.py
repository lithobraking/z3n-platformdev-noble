import requests
from ratelimit import limits


def get_endpoint(selection):
    try:
        endpoints = {
            'Organizations': 'organizations/create_many',
            'Users': 'users/create_or_update_many',
            'Tickets': 'imports/tickets/create_many'
        }
        return endpoints[selection]
    except LookupError:
        print('That selection does not exist.')

@limits(calls=45, period=60)
def send_data(datatype, email, password, payloads):
    from time import sleep
    session = requests.Session()
    url = 'https://z3n-platformdev-noble.zendesk.com/api/v2/' + get_endpoint(datatype) + '.json'
    session.headers = {'Content-Type': 'application/json'}
    status = None

    # print(email, '\n', password, '\n', datatype, '\n', url, '\n')
    for payload in payloads:
        print(payload)

        response = session.post(url, data=payload, auth=(email, password))
        if response.status_code != 200:
            status = response.status_code
            return response.status_code
        status = response.status_code
        sleep(100)

    return status
