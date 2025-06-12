import requests

access_token = "T1ANIHHS27QOCKQeHxAbIX2r3GkE"  # Use the same token

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

data = {
    "ShortCode": "600999",  # Sandbox shortcode
    "CommandID": "CustomerPayBillOnline",
    "Amount": "100",  # Use an amount matching an unpaid invoice for a tenant
    "Msisdn": "254708374149",  # Test number (always this for sandbox)
    "BillRefNumber": "A1"  # Bedsitter number
}

url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
response = requests.post(url, headers=headers, json=data)
print("Status code:", response.status_code)
print("Response:", response.json())