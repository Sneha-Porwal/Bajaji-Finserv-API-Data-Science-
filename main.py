import requests

# Step 1: Generate Webhook
generate_url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"

payload = {
    "name": "Sneha Porwal",
    "regNo": "0827CI221129",
    "email": "snehasanjay220632@acropolis.in"
}

response = requests.post(generate_url, json=payload)

if response.status_code != 200:
    print("Error generating webhook:", response.text)
    exit()

data = response.json()
webhook_url = data["webhook"]
access_token = data["accessToken"]

# Step 2: Final SQL Query
final_query = """
SELECT 
    p.AMOUNT AS SALARY,
    CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME) AS NAME,
    YEAR('2025-01-01') - YEAR(e.DOB) - 
        (DATE_FORMAT('2025-01-01', '%m%d') < DATE_FORMAT(e.DOB, '%m%d')) AS AGE,
    d.DEPARTMENT_NAME
FROM PAYMENTS p
JOIN EMPLOYEE e ON p.EMP_ID = e.EMP_ID
JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
WHERE DAY(p.PAYMENT_TIME) != 1
ORDER BY p.AMOUNT DESC
LIMIT 1;
"""

# Step 3: Submit Final Query
headers = {
    "Authorization": access_token,
    "Content-Type": "application/json"
}

submit_response = requests.post(
    webhook_url,
    json={"finalQuery": final_query.strip()},
    headers=headers
)

print("Submission status:", submit_response.status_code)
print("Response:", submit_response.text)
