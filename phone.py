from twilio.rest import Client

account_sid = "ACb195434a2b3543eb1e7dfcca6ee4af3f"
auth_token = "4e104623e4aa561756804e1e366091fd"

client = Client(account_sid, auth_token)

message = client.messages.create(
    body="Jothi",
    from_="+18668721725",  # Your Twilio phone number
    to="+14845027144",  # Recipient's phone number
)
