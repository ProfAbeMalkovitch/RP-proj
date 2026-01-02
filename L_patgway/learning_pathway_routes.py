"""Learning Pathway Routes - API endpoints for learning pathway"""

from functools import wraps
from flask import Blueprint, request, jsonify, g

import sys
from pathlib import Path
# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from accounts import account_service, AccountError
from .learning_pathway import learning_pathway_service, PathwayError

pathway_bp = Blueprint('pathway', __name__, url_prefix='/api/pathway')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if not auth or not auth.startswith('Bearer '):
            return jsonify({'error': 'Token required'}), 401
        try:
            payload = account_service.verify_token(auth.split(' ')[1])
            g.user_id = payload['user_id']
            g.user_role = payload['role']
        except AccountError as e:
            return jsonify({'error': e.message}), e.status_code
        return f(*args, **kwargs)
    return decorated

@pathway_bp.route('/me', methods=['GET'])
@token_required
def get_my_pathway():
    """Get learning pathway for current user."""
    try:
        result = learning_pathway_service.get_student_pathway(g.user_id)
        return jsonify(result), 200
    except PathwayError as e:
        return jsonify({'error': e.message}), e.status_code
    except Exception as e:
        return jsonify({'error': 'Failed to get pathway'}), 500

@pathway_bp.route('/student/<student_id>', methods=['GET'])
@token_required
def get_student_pathway(student_id):
    """Get learning pathway for a specific student (teacher/admin only)."""
    try:
        # Check if user is teacher or admin
        if g.user_role not in ['teacher', 'admin']:
            return jsonify({'error': 'Access denied'}), 403
        
        result = learning_pathway_service.get_student_pathway(student_id)
        return jsonify(result), 200
    except PathwayError as e:
        return jsonify({'error': e.message}), e.status_code
    except Exception as e:
        return jsonify({'error': 'Failed to get pathway'}), 500

