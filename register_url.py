import requests

access_token = "1HvTX02hgdtd53LObKCzJcwVgxjN"

confirmation_url = "https://2d17-197-248-199-199.ngrok-free.app/payment/c2b/confirmation/"
validation_url = "https://2d17-197-248-199-199.ngrok-free.app/payment/c2b/validation/"

# Use 600999 for sandbox, your own shortcode for production
shortcode = "600999"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

data = {
    "ShortCode": shortcode,
    "ResponseType": "Completed",
    "ConfirmationURL": confirmation_url,
    "ValidationURL": validation_url
}

url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"

response = requests.post(url, headers=headers, json=data)
print("Status code:", response.status_code)
print("Response:", response.json())