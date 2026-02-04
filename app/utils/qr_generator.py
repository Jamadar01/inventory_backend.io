import base64
import json
import requests
from urllib.parse import quote
from decouple import config


def generate_qr_code(product_data: dict) -> str:
    api_key = config('QR_API_KEY', default=None)

    qr_data = json.dumps({
        'id': product_data.get('id'),
        'name': product_data.get('name'),
        'sku': product_data.get('sku'),
        'price': str(product_data.get('price', 0))
    })

    if api_key:
        try:
            response = requests.get(
                "https://api.api-ninjas.com/v1/qrcode",
                headers={'X-Api-Key': api_key},
                params={'data': qr_data, 'format': 'png'},
                timeout=10
            )
            response.raise_for_status()
            img_base64 = base64.b64encode(response.content).decode()
            return f"data:image/png;base64,{img_base64}"
        except Exception as e:
            print(f"API error, using fallback: {e}")
            return generate_qr_code_free(qr_data)
    else:
        return generate_qr_code_free(qr_data)


def generate_qr_code_free(qr_data: str) -> str:
    encoded_data = quote(qr_data)
    api_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={encoded_data}"

    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        img_base64 = base64.b64encode(response.content).decode()
        return f"data:image/png;base64,{img_base64}"
    except Exception as e:
        raise Exception(f"Failed to generate QR code: {str(e)}")


def generate_qr_code_simple(text: str) -> str:
    api_key = config('QR_API_KEY', default=None)

    if api_key:
        try:
            response = requests.get(
                "https://api.api-ninjas.com/v1/qrcode",
                headers={'X-Api-Key': api_key},
                params={'data': text, 'format': 'png'},
                timeout=10
            )
            response.raise_for_status()
            img_base64 = base64.b64encode(response.content).decode()
            return f"data:image/png;base64,{img_base64}"
        except Exception as e:
            return generate_qr_code_free(text)
    else:
        return generate_qr_code_free(text)
