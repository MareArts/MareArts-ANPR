import requests
import time
 
def log_processing_time(start_time, step_description):
    end_time = time.time()
    processing_time = end_time - start_time
    print(f"{step_description}: Processing time: {processing_time:.2f} seconds")


def main(api_key, user_id, image_file):
    url = 'https://we303v9ck8.execute-api.eu-west-1.amazonaws.com/Prod/marearts_anpr'

    headers = {
        'Content-Type': 'image/jpeg',
        'x-api-key': api_key,
        'User-Id': user_id
    }

    with open(image_file, 'rb') as f:
        image_data = f.read()

    response = requests.post(url, headers=headers, data=image_data)

    if response.status_code == 200:
        print('Request successful')
        print('Response:', response.json())
    else:
        print(f'Failed to send request, status code: {response.status_code}')
        print('Response:', response.text)



if __name__ == "__main__":
    x_api_key = 'your-api-key'
    User_Id = 'your-user-id'
    image_files=['./21797649.jpg', "./korean_lps.jpg", "./MareArts.png", "경기37바2183_WH41931_0.jpg"]
    for image_file in image_files:
        start_time = time.time()
        main(x_api_key, User_Id, image_file)
        log_processing_time(start_time, "inferencing")
        print('---')