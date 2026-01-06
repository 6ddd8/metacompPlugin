import requests
import json
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

BASE_URL = 'https://demo-api.mce.sg/v1.0'


def request_oauth_token(body_json):
    """
    Request OAuth token endpoint
    :param body_json: JSON format request body containing client_id and client_secret
    :return: Response result
    """
    url = f'{BASE_URL}/oauth/token'
    
    # Convert JSON to dictionary
    if isinstance(body_json, str):
        params = json.loads(body_json)
    else:
        params = body_json
    
    # Prepare form-data parameters
    form_data = {
        'client_id': str(params.get('client_id', '')),
        'client_secret': str(params.get('client_secret', ''))
    }
    
    # Send POST request
    response = requests.post(url, data=form_data)
    
    return response


@app.route('/oauth/token', methods=['POST'])
def oauth_token_api():
    try:
        body_json = request.get_json()
        if not body_json:
            return jsonify({'error': 'Request body cannot be empty'}), 400
        
        response = request_oauth_token(body_json)
        
        # Filter out headers that should not be passed
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in response.headers.items() 
                   if name.lower() not in excluded_headers]
        
        return Response(response.content, status=response.status_code, headers=headers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def request_create_quotation(body_json):
    """
    Create quotation endpoint
    :param body_json: JSON format request body containing token, participantCode, clientReference, sourceCurrency, destinationCurrency
    :return: Response result
    """
    url = f'{BASE_URL}/trade/conversion/createQuotation'
    
    # Convert JSON to dictionary
    if isinstance(body_json, str):
        params = json.loads(body_json)
    else:
        params = body_json
    
    # Get token
    token = params.get('token', '')
    if not token:
        raise ValueError('Token cannot be empty')
    
    # Prepare headers
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Prepare request body data
    request_data = {
        'participantCode': params.get('participantCode', ''),
        'clientReference': params.get('clientReference', 'DynaTest'),
        'sourceCurrency': params.get('sourceCurrency', ''),
        'destinationCurrency': params.get('destinationCurrency', '')
    }
    
    # Validate required parameters
    if not request_data['participantCode']:
        raise ValueError('participantCode cannot be empty')
    if not request_data['sourceCurrency']:
        raise ValueError('sourceCurrency cannot be empty')
    if not request_data['destinationCurrency']:
        raise ValueError('destinationCurrency cannot be empty')
    
    # Send POST request
    response = requests.post(url, headers=headers, json=request_data)
    
    return response


@app.route('/trade/conversion/createQuotation', methods=['POST'])
def create_quotation_api():
    try:
        body_json = request.get_json()
        if not body_json:
            return jsonify({'error': 'Request body cannot be empty'}), 400
        
        response = request_create_quotation(body_json)
        
        # Filter out headers that should not be passed
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in response.headers.items() 
                   if name.lower() not in excluded_headers]
        
        return Response(response.content, status=response.status_code, headers=headers)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

