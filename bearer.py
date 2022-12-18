import requests

HOST = "https://api.fitbit.com"
resp = requests.get(f"{HOST}/1/user/-/ecg/list.json?beforeDate=2022-09-28&sort=asc&limit=10&offset=0", headers={
    "Authorization": f"Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzkyM0siLCJzdWIiOiJCM0tZSEgiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3bnV0IHdzbGUgd2VjZyB3c29jIHdhY3Qgd294eSB3dGVtIHd3ZWkgd2NmIHdzZXQgd2xvYyB3cmVzIiwiZXhwIjoxNjcxMzUxMTQzLCJpYXQiOjE2NzEzMjIzNDN9.cW6yh70CjhJX1RATtssz1u2YAIoNNbKXCiyTC2jHJ3I"
})

print(resp)
print(resp.text)
