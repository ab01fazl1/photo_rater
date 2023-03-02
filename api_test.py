import requests

#and example of an enrtry(sending a 2d array of urls)
urls = [
    ['https://storage.torob.com/backend-api/base/images/v_/VD/v_VD9I5v23vUUw0a.png',
     'https://storage.torob.com/backend-api/base/images/iQ/dV/iQdVPMcIB3mP4VUC.jpg',
     'https://storage.torob.com/backend-api/base/images/0p/Kf/0pKfT8EYXQXWjS96.jpg', ],
    ['https://storage1.torob.com/backend-api/base/images/Ls/Ab/LsAbdwRx9FDP7bn3.jpg',
     'https://storage.torob.com/backend-api/base/images/PM/2I/PM2ILIyxAm-CTVJK', ],
    ['https://storage1.torob.com/backend-api/base/images/vm/tZ/vmtZQpyOqGxJtU6i.jpg',
     'https://storage.torob.com/backend-api/base/images/9H/lH/9HlHHeANolHM7lNG.jpg',
     'https://storage.torob.com/backend-api/base/images/Dg/qB/DgqBeEyGgmQ_W-co.jpg',
     'https://storage.torob.com/backend-api/base/images/1S/IA/1SIAo-BgN5cfZ4A1.jpg', ],
]

#send a JSON post request
r = requests.post('http://127.0.0.1:8000/', json={
    'urls':urls
})

#print the results
print(f"Status Code: {r.status_code}, Response: {r.json()}")
