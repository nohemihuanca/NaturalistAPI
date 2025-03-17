import requests
import os
import csv
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
save_dir = os.path.expanduser('inaturalist_photos')
os.makedirs(save_dir, exist_ok=True)

# CSV file to save notes and photo details
csv_file = os.path.join(save_dir, 'notes_and_photos.csv')

def save_notes_and_photos_to_csv(data):
    with open(csv_file, 'a', newline='') as csvfile:
        fieldnames = ['user_id', 'observation_id', 'photo_id', 'photo_url', 'photo_path', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)

def download_photos_and_notes(user_id):
    url = f'https://api.inaturalist.org/v1/observations?user_id={user_id}&per_page=100'
    response = requests.get(url)
    if response.status_code == 200:
        observations = response.json()['results']
        data = []
        for obs in observations:
            observation_id = obs['id']
            note = obs.get('description', '')
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
                        data.append({
                            'user_id': user_id,
                            'observation_id': observation_id,
                            'photo_id': photo_id,
                            'photo_url': photo_url,
                            'photo_path': photo_path,
                            'description': note
                        })
                    else:
                        print(f'Failed to download photo {photo_id} for user {user_id}')
        save_notes_and_photos_to_csv(data)
    else:
        print(f'Failed to fetch observations for user {user_id}')

for user_id in user_ids:
    download_photos_and_notes(user_id)