"""Concept Mastery Routes - API endpoints for concept mastery tracking"""

from functools import wraps
from flask import Blueprint, request, jsonify, g

import sys
from pathlib import Path
# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from accounts import account_service, AccountError
from .concept_mastery import concept_mastery_service, ConceptMasteryError

concept_mastery_bp = Blueprint('concept_mastery', __name__, url_prefix='/api/concept-mastery')

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

@concept_mastery_bp.route('/me', methods=['GET'])
@token_required
def get_my_mastery():
    """Get concept mastery for current user."""
    try:
        result = concept_mastery_service.get_concept_mastery(g.user_id)
        return jsonify({
            'success': True,
            'data': result
        }), 200
    except ConceptMasteryError as e:
        return jsonify({'error': e.message}), e.status_code
    except Exception as e:
        return jsonify({'error': 'Failed to get concept mastery'}), 500

@concept_mastery_bp.route('/student/<student_id>', methods=['GET'])
@token_required
def get_student_mastery(student_id):
    """Get concept mastery for a specific student (teacher/admin only)."""
    try:
        # Check if user is teacher or admin
        if g.user_role not in ['teacher', 'admin']:
            return jsonify({'error': 'Access denied'}), 403
        
        result = concept_mastery_service.get_concept_mastery(student_id)
        return jsonify({
            'success': True,
            'data': result
        }), 200
    except ConceptMasteryError as e:
        return jsonify({'error': e.message}), e.status_code
    except Exception as e:
        return jsonify({'error': 'Failed to get concept mastery'}), 500

@concept_mastery_bp.route('/concept/<concept_name>', methods=['GET'])
@token_required
def get_concept_mastery(concept_name):
    """Get mastery for a specific concept for current user."""
    try:
        result = concept_mastery_service.get_concept_mastery_by_name(g.user_id, concept_name)
        if result:
            return jsonify({
                'success': True,
                'data': result
            }), 200
        else:
            return jsonify({
                'error': 'Concept mastery not found',
                'message': f'No mastery data found for concept: {concept_name}'
            }), 404
    except ConceptMasteryError as e:
        return jsonify({'error': e.message}), e.status_code
    except Exception as e:
        return jsonify({'error': 'Failed to get concept mastery'}), 500

