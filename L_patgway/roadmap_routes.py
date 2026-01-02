"""Roadmap Routes - API endpoints for learning roadmap and mind map"""

from functools import wraps
from flask import Blueprint, request, jsonify, g

import sys
from pathlib import Path
# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from accounts import account_service, AccountError
from .roadmap_service import roadmap_service, RoadmapError
from .concept_mastery import concept_mastery_service

roadmap_bp = Blueprint('roadmap', __name__, url_prefix='/api/roadmap')

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

@roadmap_bp.route('/me', methods=['GET'])
@token_required
def get_my_roadmap():
    """Get learning roadmap for current user."""
    try:
        result = roadmap_service.get_roadmap(g.user_id)
        return jsonify(result), 200
    except RoadmapError as e:
        return jsonify({'error': e.message}), e.status_code
    except Exception as e:
        return jsonify({'error': 'Failed to get roadmap'}), 500

@roadmap_bp.route('/mindmap', methods=['GET'])
@token_required
def get_mindmap():
    """Get mind map data showing weak areas."""
    try:
        weak_areas = roadmap_service.identify_weak_areas(g.user_id)
        mastery_data = concept_mastery_service.get_concept_mastery(g.user_id)
        
        # Organize for mind map visualization
        mindmap_data = {
            'weak_areas': weak_areas,
            'all_concepts': mastery_data.get('concepts', []),
            'strong_areas': [
                c for c in mastery_data.get('concepts', [])
                if c['mastery_percentage'] >= 75
            ],
            'average_mastery': mastery_data.get('average_mastery', 0)
        }
        
        return jsonify({
            'success': True,
            'data': mindmap_data
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get mind map'}), 500

@roadmap_bp.route('/student/<student_id>', methods=['GET'])
@token_required
def get_student_roadmap(student_id):
    """Get roadmap for a specific student (teacher/admin only)."""
    try:
        if g.user_role not in ['teacher', 'admin']:
            return jsonify({'error': 'Access denied'}), 403
        
        result = roadmap_service.get_roadmap(student_id)
        return jsonify(result), 200
    except RoadmapError as e:
        return jsonify({'error': e.message}), e.status_code
    except Exception as e:
        return jsonify({'error': 'Failed to get roadmap'}), 500

