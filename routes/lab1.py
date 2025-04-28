from flask import Blueprint, jsonify, request
import uuid
from functools import wraps

lab1_routes = Blueprint('lab1', __name__)

# Simulated database
users = {
    "1": {
        "id": "1",
        "name": "Jordan",
        "walletAddress": "JrdN1XyBfXJKUd5dNoYz9F4UdaZ1pEMVr9Jv5e7SSYp",
        "balance": "45.32 SOL",
        "transactions": [
            {
                "id": "tx1",
                "type": "Send",
                "amount": "5.2 SOL",
                "timestamp": "2025-04-15 14:32:11",
                "status": "Confirmed",
                "signature": "5KtP9UYpn...",
            },
            {
                "id": "tx2",
                "type": "Receive",
                "amount": "12.0 SOL",
                "timestamp": "2025-04-14 09:15:43",
                "status": "Confirmed",
                "signature": "3xQm7UYzr...",
            },
            {
                "id": "tx3",
                "type": "NFT Mint",
                "amount": "0.05 SOL",
                "timestamp": "2025-04-10 18:22:05",
                "status": "Confirmed",
                "signature": "9pLm2RYxq...",
            },
        ],
        "nfts": [
            {
                "id": "nft1",
                "name": "Solana Monkey #1234",
                "collection": "SMB",
                "image": "/placeholder.svg?height=150&width=150",
            },
            {
                "id": "nft2",
                "name": "DeGods #5678",
                "collection": "DeGods",
                "image": "/placeholder.svg?height=150&width=150",
            },
        ],
        "privateApiKey": "sk_live_jordan_12345abcdef",
    },
    "2": {
        "id": "2",
        "name": "Taylor",
        "walletAddress": "TayX7ZpqRt2PtVk5uYs9KfmjJhAzDXpR8iKvxNK3YFD",
        "balance": "128.75 SOL",
        "transactions": [
            {
                "id": "tx4",
                "type": "Swap",
                "amount": "10.5 SOL → 420 USDC",
                "timestamp": "2025-04-16 11:22:33",
                "status": "Confirmed",
                "signature": "7RtY9UYpn...",
            },
            {
                "id": "tx5",
                "type": "Stake",
                "amount": "50.0 SOL",
                "timestamp": "2025-04-12 16:44:21",
                "status": "Confirmed",
                "signature": "2xZm7UYzr...",
            },
        ],
        "nfts": [
            {
                "id": "nft3",
                "name": "Okay Bears #9012",
                "collection": "Okay Bears",
                "image": "/placeholder.svg?height=150&width=150",
            },
        ],
        "privateApiKey": "sk_live_taylor_67890ghijkl",
    },
    "3": {
        "id": "3",
        "name": "Morgan",
        "walletAddress": "MrgN5ZpqRt2PtVk5uYs9KfmjJhAzDXpR8iKvxNK3YFD",
        "balance": "352.18 SOL",
        "transactions": [
            {
                "id": "tx6",
                "type": "NFT Purchase",
                "amount": "35.0 SOL",
                "timestamp": "2025-04-17 09:12:45",
                "status": "Confirmed",
                "signature": "8TyZ9UYpn...",
            },
        ],
        "nfts": [
            {
                "id": "nft4",
                "name": "Solana Monkey #4321",
                "collection": "SMB",
                "image": "/placeholder.svg?height=150&width=150",
            },
            {
                "id": "nft5",
                "name": "DeGods #8765",
                "collection": "DeGods",
                "image": "/placeholder.svg?height=150&width=150",
            },
        ],
        "privateApiKey": "sk_live_morgan_mnopqrstuv",
    },
}

# Simulated sessions
sessions = {}

# VULNERABLE implementation - no authentication check
@lab1_routes.route('/vulnerable/users/<user_id>', methods=['GET'])
def get_user_vulnerable(user_id):
    """
    VULNERABLE: This endpoint has an IDOR vulnerability as it doesn't check 
    if the requester is authorized to access the requested user's data
    """
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify(users[user_id])

# FIXED implementation - with authentication and authorization
def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_token = request.headers.get('Authorization')
        if not auth_token or auth_token not in sessions:
            return jsonify({"error": "Authentication required"}), 401
        
        # Add the user to the request context
        request.user = sessions[auth_token]
        return f(*args, **kwargs)
    return decorated_function

@lab1_routes.route('/fixed/login', methods=['POST'])
def login():
    """Login endpoint for the fixed implementation"""
    data = request.json
    user_id = data.get('userId', '1')  # Default to user 1 for demo
    
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    
    # Create a session token
    token = str(uuid.uuid4())
    sessions[token] = users[user_id]
    
    return jsonify({
        "token": token,
        "user": {
            "id": users[user_id]["id"],
            "name": users[user_id]["name"]
        }
    })

@lab1_routes.route('/fixed/users/<user_id>', methods=['GET'])
@authenticate
def get_user_fixed(user_id):
    """
    FIXED: This endpoint checks if the authenticated user is authorized
    to access the requested user's data
    """
    # Check if the authenticated user is authorized to access this data
    if request.user["id"] != user_id:
        return jsonify({
            "error": "Access denied: You can only access your own data"
        }), 403
    
    return jsonify(request.user)
