import requests
import os

# User IDs

'''
List of users in project 228504 
https://api.inaturalist.org/v1/projects/228504/members?skip_counts=false


crono_secuencia_2 - user_id 9000660
crono_secuencia_3 - user_id 9000828


 
Observation created by userid crono_secuencia_2

https://api.inaturalist.org/v1/observations?user_id=9000660&order=desc&order_by=created_at

Observation created by userid crono_secuencia_3 

https://api.inaturalist.org/v1/observations?user_id=9000828&order=desc&order_by=created_at
'''
user_ids = [9000660, 9000828]

# Directory to save photos
save_dir = '~/Desktop/inaturalist_photos'
os.makedirs(save_dir, exist_ok=True)

def download_photos(user_id):
    url = f'https://api.inaturalist.org/v1/observations?user_id={user_id}&per_page=100'
    response = requests.get(url)
    if response.status_code == 200:
        observations = response.json()['results']
        for obs in observations:
            if 'photos' in obs:
                for photo in obs['photos']:
                    photo_url = photo['url'].replace('square', 'original')
                    photo_id = photo['id']
                    photo_response = requests.get(photo_url)
                    if photo_response.status_code == 200:
                        photo_path = os.path.join(save_dir, f'{user_id}_{photo_id}.jpg')
                        with open(photo_path, 'wb') as f:
                            f.write(photo_response.content)
                        print(f'Downloaded photo {photo_id} for user {user_id}')
                    else:
                        print(f'Failed to download photo {photo_id} for user {user_id}')
    else:
        print(f'Failed to fetch observations for user {user_id}')

for user_id in user_ids:
    download_photos(user_id)