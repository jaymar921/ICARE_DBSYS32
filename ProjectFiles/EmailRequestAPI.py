import requests


def sendEmail(email: str, name: str):
    headers = {
        'X-MAGICBELL-API-SECRET': 'AYJ8JBKQsb/0TxlW+xeyK/hobfKHR8cJQH/av1o8',
        'X-MAGICBELL-API-KEY': '9c2ed099185f55a8817bd77087f91d97c29d633b',
    }

    data = {
        "notification": {
            "title": "Welcome to iCare",
            "content": f"Hello {name},\nYou're officially registered in iCare Pet Services",
            "category": "new_message",
            "action_url": "https://developer.magicbell.com",
            "recipients": [{
                "email": f"{email}"
            }],
            "custom_attributes": {
                "order": {
                    "id": "1202983",
                    "title": "A title you can use in your templates"
                }
            }
        }
    }

    response = requests.post('https://api.magicbell.com/notifications', headers=headers, json=data)
