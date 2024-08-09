import requests
import sys

# Set the output encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# API token
API_TOKEN = ''

def fetch_data(api_token, endpoint):
    base_url = f'https://metricsv8.saasoptics.com/bandwango/api/v1.0/{endpoint}/'
    headers = {
        'Authorization': f'Token {api_token}',
        'Accept': 'application/json'
    }

    params = {'page': 1}  # Start from the first page
    all_data = []

    while True:
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            all_data.extend(data['results'])
            print(f"Page {params['page']}: Retrieved {len(data['results'])} items from {endpoint}")

            # Check if there's a next page
            if data.get('next'):
                params['page'] += 1
            else:
                break
        else:
            print(f'Error fetching data from {endpoint}: {response.status_code} - {response.text}')
            break

    return all_data

def get_customer_name(api_token, customer_id):
    base_url = f'https://metricsv8.saasoptics.com/bandwango/api/v1.0/customers/{customer_id}/'
    headers = {
        'Authorization': f'Token {api_token}',
        'Accept': 'application/json'
    }

    response = requests.get(base_url, headers=headers)
    if response.status_code == 200:
        customer = response.json()
        return customer.get('name')
    else:
        print(f'Error retrieving customer {customer_id}: {response.status_code} - {response.text}')
        return None

def print_payment_info(api_token, payment):
    customer_id = payment['customer']
    customer_name = get_customer_name(api_token, customer_id)
    print(f"Customer: {customer_name} (ID: {customer_id})")
    print(f"Payment ID: {payment['id']}, Number: {payment['number']}, Date: {payment['date']}")
    print(f"Amount: {payment['local_amount']} {payment['currency']}, Status: {payment['status']}")
    print(f"Reference Number: {payment['reference_number']}, Description: {payment['description']}")
    print(f"Source System: {payment['source_system']}, Created on: {payment['source_created']}")
    print()

def main():
    payments = fetch_data(API_TOKEN, 'payments')
    refunds = fetch_data(API_TOKEN, 'refunds')

    print("\nPayments Received:")
    for payment in payments:
        print_payment_info(API_TOKEN, payment)

    print("Refunds/Credits Issued:")
    for refund in refunds:
        print_payment_info(API_TOKEN, refund)

if __name__ == '__main__':
    main()
