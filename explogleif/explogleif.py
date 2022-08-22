import requests

def count_all_lei():
    url = 'https://api.gleif.org/api/v1/lei-records'
    
    headers = {
        'Accept': 'application/vnd.api+json'
        }
    
    payload={
    'page[number]': 1,
    'page[size]': 1 # one page per lei
    }
    
    response = requests.request('GET',url,headers=headers, data=payload).json()
    
    # since we have one page per lei, number of pages == number of lei
    return response['meta']['pagination']['total']
    