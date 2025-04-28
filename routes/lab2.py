from flask import Blueprint, jsonify, request
import requests
from urllib.parse import urlparse
import ipaddress
import socket

lab2_routes = Blueprint('lab2', __name__)

# VULNERABLE implementation - no URL validation
@lab2_routes.route('/vulnerable/fetch-metadata', methods=['POST'])
def fetch_metadata_vulnerable():
    """
    VULNERABLE: This endpoint has an SSRF vulnerability as it doesn't validate
    the URL before making the request
    """
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    try:
        # VULNERABLE: No validation of URL before making the request
        response = requests.get(url, timeout=5)
        metadata = response.json()
        
        return jsonify({
            "success": True,
            "metadata": metadata
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to fetch metadata: {str(e)}"
        }), 500

# FIXED implementation - with URL validation
@lab2_routes.route('/fixed/fetch-metadata', methods=['POST'])
def fetch_metadata_fixed():
    """
    FIXED: This endpoint validates the URL before making the request
    """
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    # Validate URL before making the request
    validation_result = is_url_allowed(url)
    if not validation_result['allowed']:
        return jsonify({
            "success": False,
            "error": f"URL validation failed: {validation_result['reason']}"
        }), 400
    
    try:
        response = requests.get(url, timeout=5)
        metadata = response.json()
        
        return jsonify({
            "success": True,
            "metadata": metadata
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to fetch metadata: {str(e)}"
        }), 500

def is_url_allowed(url_string):
    """
    Validates if a URL is allowed based on security criteria
    """
    ALLOWED_DOMAINS = [
        'ipfs.io',
        'arweave.net',
        'nftstorage.link',
        'example.com'
    ]
    
    try:
        # Parse the URL
        url = urlparse(url_string)
        
        # Only allow http and https protocols
        if url.scheme not in ['http', 'https']:
            return {
                'allowed': False,
                'reason': 'Only HTTP and HTTPS protocols are allowed'
            }
        
        # Get the domain
        domain = url.netloc.lower()
        
        # Check if domain is in allowlist
        if not any(domain == d or domain.endswith(f'.{d}') for d in ALLOWED_DOMAINS):
            return {
                'allowed': False,
                'reason': f'Domain not in allowlist: {domain}'
            }
        
        # Prevent access to internal IP addresses
        try:
            ip = socket.gethostbyname(domain)
            ip_obj = ipaddress.ip_address(ip)
            
            if ip_obj.is_private or ip_obj.is_loopback:
                return {
                    'allowed': False,
                    'reason': f'IP address is private or loopback: {ip}'
                }
        except:
            # Not an IP address or couldn't resolve, continue with domain validation
            pass
        
        return {'allowed': True}
    except Exception as e:
        return {
            'allowed': False,
            'reason': f'Invalid URL format: {str(e)}'
        }
