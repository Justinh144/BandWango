import requests
import datetime

def fetch_contracts(api_url, api_token, customer_id=None):
    headers = {
        'Authorization': f'Token {api_token}',
        'Accept': 'application/json'
    }
    
    params = {
        'page': 1,  # Start from the first page
        'sort': 'modified',  # Sort by the 'modified' field
        'created__gte': '2023-01-01T00:00:00.000000',  # Customize this date as needed
        'created__lte': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000000')
    }
    
    if customer_id:
        params['customer'] = customer_id  # Filter by customer ID if provided
    
    all_contracts = []
    
    while True:
        response = requests.get(api_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            all_contracts.extend(data['results'])
            print(f"Page {params['page']}: Retrieved {len(data['results'])} contracts")
            
            if data.get('next'):
                params['page'] += 1
            else:
                break
        else:
            print(f"Error: {response.status_code} - {response.text}")
            break

    return all_contracts

def fetch_revenue_entries(api_url, api_token, contract_id):
    headers = {
        'Authorization': f'Token {api_token}',
        'Accept': 'application/json'
    }
    
    params = {
        'page': 1,  # Start from the first page
        'contract': contract_id  # Filter by contract ID
    }
    
    all_revenue_entries = []
    
    while True:
        response = requests.get(api_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            all_revenue_entries.extend(data['results'])
            if data.get('next'):
                params['page'] += 1
            else:
                break
        else:
            print(f"Error fetching revenue entries for contract {contract_id}: {response.status_code} - {response.text}")
            break

    return all_revenue_entries

def calculate_total_revenue(revenue_entries):
    total_revenue = 0.0
    for entry in revenue_entries:
        local_amount = float(entry['local_amount'])
        total_revenue += local_amount
    return total_revenue

def get_subscription_status(contract):
    cancelled = contract.get('cancelled', False)
    is_autorenewal = contract.get('is_autorenewal', False)
    
    if cancelled:
        return "Canceled"
    elif is_autorenewal:
        return "Auto-renewal"
    else:
        return "Active"

def format_contract(contract, total_revenue):
    # Prepare a formatted string for each contract
    email = contract['email'] if contract['email'] else "No email provided"
    subscription_status = get_subscription_status(contract)
    return (f"ID: {contract['id']}, Number: {contract['number']}, "
            f"Status: {subscription_status}, Active: {contract['is_active']}, "
            f"Created: {contract['created']}, "
            f"Modified: {contract['modified']}, Total Revenue: ${total_revenue:.2f}")

def main():
    API_URL_CONTRACTS = 'https://metricsv8.saasoptics.com/bandwango/api/v1.0/contracts/'
    API_URL_REVENUE_ENTRIES = 'https://metricsv8.saasoptics.com/bandwango/api/v1.0/revenue_entries/'
    API_TOKEN = ''  # Replace with your actual API token
    CUSTOMER_ID = ''  # Keep Blank

    contracts = fetch_contracts(API_URL_CONTRACTS, API_TOKEN, CUSTOMER_ID)
    print(f"Total contracts retrieved: {len(contracts)}")
    
    for contract in contracts:
        revenue_entries = fetch_revenue_entries(API_URL_REVENUE_ENTRIES, API_TOKEN, contract['id'])
        total_revenue = calculate_total_revenue(revenue_entries)
        print(format_contract(contract, total_revenue))  # Print each contract's formatted details

if __name__ == "__main__":
    main()
