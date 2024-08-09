import requests
import sys

# Set the output encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# API token
API_TOKEN = ''

def list_all_customers(api_token):
    base_url = 'https://metricsv8.saasoptics.com/bandwango/api/v1.0/customers/'
    headers = {
        'Authorization': f'Token {api_token}',
        'Accept': 'application/json'
    }

    params = {
        'page': 1  # Start from the first page
    }

    all_customers = []

    while True:
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            all_customers.extend(data['results'])

            # Log the number of results and current page
            print(f"Page {params['page']}: Retrieved {len(data['results'])} customers")

            # Check if there's a next page
            if data.get('next'):
                params['page'] += 1
            else:
                break
        else:
            print(f'Error: {response.status_code} - {response.text}')
            break

    print(f"Total customers retrieved: {len(all_customers)}")

    for customer in all_customers:
        customer_id = customer.get('id')
        customer_name = customer.get('name')
        email = customer.get('email')
        is_active = customer.get('is_active')
        print(f'Customer ID: {customer_id}, Name: {customer_name}, Email: {email}, Active: {is_active}')

if __name__ == "__main__":
    list_all_customers(API_TOKEN)
