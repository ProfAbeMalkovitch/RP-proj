import os
import uuid
import json
import re
import csv
import random
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, send_from_directory, Response
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF

# MongoDB Setup
try:
    from pymongo import MongoClient
    from bson import ObjectId
    MONGO_URI = "mongodb+srv://cursorrp_db_user:ka1r5cs2fPu1fcIk@cluster0.7fr4den.mongodb.net/?appName=Cluster0"
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client.rpelearn_db
    MONGO_CONNECTED = True
    print("MongoDB connected successfully!")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    MONGO_CONNECTED = False
    db = None

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['EXTRACTED_FOLDER'] = 'extracted'
app.config['ECESE_FOLDER'] = 'ecese_outputs'

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['EXTRACTED_FOLDER'], exist_ok=True)
os.makedirs(app.config['ECESE_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ==================== PDF EXTRACTION FUNCTIONS ====================

def extract_data_from_pdf(pdf_path, session_id):
    """Basic PDF extraction for text and images."""
    try:
        image_dir = os.path.join(app.config['EXTRACTED_FOLDER'], session_id, 'images')
        os.makedirs(image_dir, exist_ok=True)
        
        doc = fitz.open(pdf_path)
        num_pages = doc.page_count
        
        pages_data = []
        total_images = 0
        
        for page_num in range(num_pages):
            page = doc.load_page(page_num)
            text = page.get_text()
            
            image_list = page.get_images(full=True)
            page_images = []
            
            if image_list:
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    image_filename = f"page{page_num+1}_img{img_index+1}.{image_ext}"
                    image_path = os.path.join(image_dir, image_filename)
                    with open(image_path, "wb") as img_file:
                        img_file.write(image_bytes)
                    
                    page_images.append({
                        'filename': image_filename,
                        'url': f'/extracted/{session_id}/images/{image_filename}'
                    })
                    total_images += 1
            
            pages_data.append({
                'page_number': page_num + 1,
                'text': text.strip() if text else '',
                'images': page_images
            })
        
        doc.close()
        
        return {
            'success': True,
            'total_pages': num_pages,
            'total_images': total_images,
            'pages': pages_data
        }

    except FileNotFoundError:
        return {'success': False, 'error': f"File not found."}
    except Exception as e:
        return {'success': False, 'error': str(e)}


# ==================== ECESE CORE MODULES ====================

class TeachersGuideExtractor:
    """
    Extracts scope keywords, syllabus topics, and learning objectives from Teacher's Guide/Syllabus PDF.
    Used to filter and align textbook content with curriculum requirements.
    """
    
    # Patterns to identify important syllabus content
    SYLLABUS_PATTERNS = {
        'topic': [
            r'^(?:topic|unit|chapter|module)\s*[\d.:]+\s*[:\-–]?\s*(.+)',
            r'^(\d+\.)\s+([A-Z][^\n]+)',
        ],
        'objective': [
            r'(?:students?\s*(?:will|should)\s*(?:be\s*able\s*to)?)\s*([^.]+\.)',
            r'(?:learning\s*(?:objectives?|outcomes?))[:\s]*([^.]+\.)',
        ],
        'competency': [
            r'(?:competenc(?:y|ies))[:\s]*([^.]+\.)',
            r'(?:skills?)[:\s]*([^.]+\.)',
        ],
        'assessment': [
            r'(?:assessment|evaluation)[:\s]*([^.]+\.)',
        ],
    }
    
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.extracted_topics = []
        self.extracted_keywords = []
        self.learning_outcomes = []
        self.full_text = ""
    
    def extract(self):
        """Extract curriculum scope from teacher's guide."""
        try:
            doc = fitz.open(self.pdf_path)
            
            all_text = []
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                blocks = page.get_text("dict")["blocks"]
                
                for block in blocks:
                    if "lines" in block:
                        for line in block["lines"]:
                            text = ""
                            font_size = 0
                            is_bold = False
                            
                            for span in line["spans"]:
                                text += span["text"]
                                font_size = max(font_size, span["size"])
                                if "bold" in span.get("font", "").lower():
                                    is_bold = True
                            
                            text = text.strip()
                            if text:
                                all_text.append(text)
                                
                                # Extract topics from headings
                                if is_bold or font_size > 12:
                                    self._extract_topic(text)
            
            doc.close()
            self.full_text = ' '.join(all_text)
            
            # Extract keywords from full text
            self._extract_keywords()
            self._extract_learning_outcomes()
            
            return True
            
        except Exception as e:
            print(f"Error extracting teacher's guide: {e}")
            return False
    
    def _extract_topic(self, text):
        """Extract topic from text."""
        for pattern in self.SYLLABUS_PATTERNS['topic']:
            match = re.match(pattern, text, re.IGNORECASE)
            if match:
                topic = match.group(1) if len(match.groups()) == 1 else match.group(2)
                if topic and len(topic) > 3:
                    self.extracted_topics.append(topic.strip())
                return
        
        # Also capture standalone headings
        if len(text) < 100 and text[0].isupper():
            words = text.split()
            if 2 <= len(words) <= 8:
                self.extracted_topics.append(text)
    
    def _extract_keywords(self):
        """Extract important keywords from the guide."""
        # Common educational keywords
        keyword_patterns = [
            r'\b(algebra|geometry|calculus|trigonometry|statistics)\b',
            r'\b(equation|function|variable|expression|formula)\b',
            r'\b(photosynthesis|respiration|ecology|genetics|evolution)\b',
            r'\b(force|energy|motion|electricity|magnetism)\b',
            r'\b(grammar|vocabulary|comprehension|writing|literature)\b',
            r'\b(history|geography|economics|civics|culture)\b',
        ]
        
        text_lower = self.full_text.lower()
        
        for pattern in keyword_patterns:
            matches = re.findall(pattern, text_lower)
            self.extracted_keywords.extend(matches)
        
        # Also extract capitalized terms (likely key concepts)
        concept_matches = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b', self.full_text)
        for concept in concept_matches:
            if len(concept) > 3 and concept.lower() not in ['the', 'and', 'for', 'this', 'that']:
                self.extracted_keywords.append(concept.lower())
        
        # Deduplicate
        self.extracted_keywords = list(set(self.extracted_keywords))
    
    def _extract_learning_outcomes(self):
        """Extract learning outcomes/objectives."""
        for pattern in self.SYLLABUS_PATTERNS['objective']:
            matches = re.findall(pattern, self.full_text, re.IGNORECASE)
            self.learning_outcomes.extend([m.strip() for m in matches if len(m) > 10])
    
    def get_scope_data(self):
        """Return extracted scope data."""
        return {
            'topics': self.extracted_topics[:50],  # Limit
            'keywords': self.extracted_keywords[:100],
            'learning_outcomes': self.learning_outcomes[:30],
            'has_content': bool(self.extracted_topics or self.extracted_keywords)
        }


class ContentParsingUnit:
    """
    Module 1: Content Parsing Unit
    Uses NLP techniques to parse PDFs and extract structural elements.
    Identifies headings, subheadings, tables, figures, and reconstructs logical structure.
    """
    
    # Patterns for structural element detection
    STRUCTURAL_PATTERNS = {
        'chapter': [
            r'^(?:chapter|unit|module)\s*[\d.:]+\s*[:\-–]?\s*(.+)',
            r'^(?:CHAPTER|UNIT|MODULE)\s*[\d.:]+\s*[:\-–]?\s*(.+)',
        ],
        'section': [
            r'^(\d+\.)\s+([A-Z][^.]+)',
            r'^([A-Z][A-Z\s]{3,})$',
        ],
        'subsection': [
            r'^(\d+\.\d+\.?)\s+(.+)',
            r'^([a-z]\))\s+(.+)',
        ],
        'learning_objective': [
            r'(?:learning\s*objectives?|outcomes?|goals?)[:\s]*',
            r'(?:by\s*the\s*end|after\s*(?:this|completing))[^:]*:',
            r'students?\s*(?:will|should)\s*(?:be\s*able\s*to)?',
        ],
        'definition': [
            r'^(?:definition|key\s*term|glossary)[:\s]*',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*[:\-–]\s*(.+)',
        ],
        'example': [
            r'^(?:example|e\.g\.|for\s*instance|illustration)[:\s]*',
        ],
        'table': [
            r'(?:table|figure)\s*\d+[:\.]?\s*(.+)',
        ],
        'summary': [
            r'^(?:summary|conclusion|key\s*points?|recap|review)[:\s]*',
        ],
    }
    
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.raw_blocks = []
        self.structural_elements = {
            'chapters': [],
            'sections': [],
            'subsections': [],
            'tables': [],
            'figures': [],
            'definitions': [],
            'examples': [],
        }
        self.metadata = {}
    
    def parse_document(self):
        """Parse PDF and extract all structural elements."""
        try:
            doc = fitz.open(self.pdf_path)
            
            # Extract metadata
            self.metadata = {
                'title': doc.metadata.get('title', 'Untitled Document'),
                'author': doc.metadata.get('author', 'Unknown'),
                'subject': doc.metadata.get('subject', ''),
                'keywords': doc.metadata.get('keywords', ''),
                'page_count': doc.page_count,
                'creation_date': doc.metadata.get('creationDate', ''),
            }
            
            # Extract text blocks with formatting info
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                blocks = page.get_text("dict")["blocks"]
                
                for block in blocks:
                    if "lines" in block:
                        for line in block["lines"]:
                            text = ""
                            font_size = 0
                            font_name = ""
                            is_bold = False
                            is_italic = False
                            
                            for span in line["spans"]:
                                text += span["text"]
                                font_size = max(font_size, span["size"])
                                font_name = span.get("font", "")
                                if "bold" in font_name.lower() or "black" in font_name.lower():
                                    is_bold = True
                                if "italic" in font_name.lower() or "oblique" in font_name.lower():
                                    is_italic = True
                            
                            if text.strip():
                                self.raw_blocks.append({
                                    'text': text.strip(),
                                    'font_size': font_size,
                                    'font_name': font_name,
                                    'is_bold': is_bold,
                                    'is_italic': is_italic,
                                    'page': page_num + 1,
                                    'bbox': block['bbox'],
                                    'block_type': self._classify_block_type(text.strip(), font_size, is_bold)
                                })
            
            doc.close()
            self._identify_structural_elements()
            return True
            
        except Exception as e:
            print(f"Error parsing document: {e}")
            return False
    
    def _classify_block_type(self, text, font_size, is_bold):
        """Classify block type based on patterns and formatting."""
        # Check for chapter
        for pattern in self.STRUCTURAL_PATTERNS['chapter']:
            if re.match(pattern, text, re.IGNORECASE):
                return 'chapter'
        
        # Check for section
        for pattern in self.STRUCTURAL_PATTERNS['section']:
            if re.match(pattern, text):
                return 'section'
        
        # Check for subsection
        for pattern in self.STRUCTURAL_PATTERNS['subsection']:
            if re.match(pattern, text):
                return 'subsection'
        
        # Check for table/figure references
        for pattern in self.STRUCTURAL_PATTERNS['table']:
            if re.match(pattern, text, re.IGNORECASE):
                return 'table_reference'
        
        # Bold large text likely a heading
        if is_bold and font_size > 12:
            return 'heading'
        
        return 'paragraph'
    
    def _identify_structural_elements(self):
        """Identify and categorize all structural elements."""
        if not self.raw_blocks:
            return
            
        # Calculate average font size for comparison
        font_sizes = [b['font_size'] for b in self.raw_blocks if b['font_size'] > 0]
        avg_font_size = sum(font_sizes) / len(font_sizes) if font_sizes else 12
        
        for block in self.raw_blocks:
            if block['block_type'] == 'chapter' or (block['font_size'] > avg_font_size * 1.4 and block['is_bold']):
                self.structural_elements['chapters'].append(block)
            elif block['block_type'] == 'section' or (block['font_size'] > avg_font_size * 1.2 and block['is_bold']):
                self.structural_elements['sections'].append(block)
            elif block['block_type'] == 'subsection':
                self.structural_elements['subsections'].append(block)
    
    def get_parsed_content(self):
        """Return parsed content with structure."""
        return {
            'metadata': self.metadata,
            'raw_blocks': self.raw_blocks,
            'structural_elements': self.structural_elements
        }


class ScopeFilteringModule:
    """
    Module 2: Scope Filtering Module
    Cross-checks extracted content against teacher's guide and syllabus taxonomies.
    Filters content to ensure curriculum alignment and flags off-topic material.
    """
    
    def __init__(self, scope_keywords=None, syllabus_topics=None, grade_level=None):
        self.scope_keywords = [k.lower().strip() for k in (scope_keywords or [])]
        self.syllabus_topics = syllabus_topics or []
        self.grade_level = grade_level
        self.filtered_content = []
        self.flagged_content = []  # Off-topic material
        self.alignment_score = 0
    
    def filter_content(self, parsed_blocks):
        """Filter content based on curriculum scope."""
        if not self.scope_keywords:
            # No filtering if no scope specified
            return parsed_blocks, [], 100
        
        filtered = []
        flagged = []
        matched_count = 0
        
        for block in parsed_blocks:
            text_lower = block['text'].lower()
            
            # Check if block matches any scope keyword
            is_relevant = any(keyword in text_lower for keyword in self.scope_keywords)
            
            # Also check structural elements (always keep headings)
            is_structural = block.get('block_type') in ['chapter', 'section', 'subsection', 'heading']
            
            if is_relevant or is_structural:
                block['scope_status'] = 'aligned'
                filtered.append(block)
                matched_count += 1
            else:
                # Check if it's connected to relevant content (within 3 blocks)
                block['scope_status'] = 'flagged'
                flagged.append(block)
        
        # Calculate alignment score
        total = len(parsed_blocks)
        self.alignment_score = (matched_count / total * 100) if total > 0 else 0
        
        self.filtered_content = filtered
        self.flagged_content = flagged
        
        return filtered, flagged, self.alignment_score
    
    def get_scope_report(self):
        """Generate scope adherence report."""
        return {
            'total_blocks': len(self.filtered_content) + len(self.flagged_content),
            'aligned_blocks': len(self.filtered_content),
            'flagged_blocks': len(self.flagged_content),
            'alignment_score': round(self.alignment_score, 2),
            'scope_keywords': self.scope_keywords,
            'grade_level': self.grade_level
        }


class StructuringEngine:
    """
    Module 3: Structuring Engine
    Organizes filtered content into hierarchical format:
    Subject → Topic → Subtopic → Learning Objectives
    Generates micro-lessons with metadata (difficulty, study time).
    """
    
    # Bloom's Taxonomy action verbs for learning objectives
    BLOOMS_TAXONOMY = {
        'remember': {
            'verbs': ['define', 'list', 'recall', 'identify', 'name', 'state', 'describe', 'recognize', 'label', 'match'],
            'level': 1,
            'description': 'Recall facts and basic concepts'
        },
        'understand': {
            'verbs': ['explain', 'summarize', 'interpret', 'classify', 'compare', 'discuss', 'paraphrase', 'predict', 'translate'],
            'level': 2,
            'description': 'Explain ideas or concepts'
        },
        'apply': {
            'verbs': ['apply', 'demonstrate', 'solve', 'use', 'implement', 'execute', 'show', 'illustrate', 'calculate'],
            'level': 3,
            'description': 'Use information in new situations'
        },
        'analyze': {
            'verbs': ['analyze', 'differentiate', 'examine', 'contrast', 'investigate', 'organize', 'deconstruct', 'attribute'],
            'level': 4,
            'description': 'Draw connections among ideas'
        },
        'evaluate': {
            'verbs': ['evaluate', 'assess', 'critique', 'judge', 'justify', 'recommend', 'defend', 'prioritize', 'rate'],
            'level': 5,
            'description': 'Justify a decision or course of action'
        },
        'create': {
            'verbs': ['create', 'design', 'develop', 'construct', 'produce', 'generate', 'plan', 'compose', 'formulate'],
            'level': 6,
            'description': 'Produce new or original work'
        }
    }
    
    # Difficulty mapping based on grade level
    DIFFICULTY_MAPPING = {
        'grade-6': {'base': 1, 'words_per_min': 120},
        'grade-7': {'base': 1, 'words_per_min': 130},
        'grade-8': {'base': 2, 'words_per_min': 140},
        'grade-9': {'base': 2, 'words_per_min': 150},
        'grade-10': {'base': 3, 'words_per_min': 160},
        'grade-11': {'base': 3, 'words_per_min': 170},
        'undergraduate': {'base': 4, 'words_per_min': 200},
        'postgraduate': {'base': 5, 'words_per_min': 220},
    }
    
    def __init__(self, subject_name="", grade_level=""):
        self.subject_name = subject_name
        self.grade_level = grade_level
        self.hierarchy = {
            'subject': subject_name,
            'topics': []
        }
        self.learning_objectives = []
        self.key_terms = []
        self.micro_lessons = []
        self.tables_figures = []
    
    def structure_content(self, filtered_blocks, metadata):
        """Organize content into hierarchical structure."""
        if not filtered_blocks:
            return
        
        # Build hierarchy from structural elements
        current_topic = None
        current_subtopic = None
        current_content = []
        
        # Calculate font statistics
        font_sizes = [b['font_size'] for b in filtered_blocks if b['font_size'] > 0]
        avg_font = sum(font_sizes) / len(font_sizes) if font_sizes else 12
        
        for block in filtered_blocks:
            text = block['text']
            font_size = block['font_size']
            is_bold = block.get('is_bold', False)
            block_type = block.get('block_type', 'paragraph')
            
            # Detect topic (chapter/major section)
            if block_type == 'chapter' or (font_size > avg_font * 1.4 and is_bold):
                # Save previous topic
                if current_topic:
                    if current_subtopic:
                        current_subtopic['content'] = '\n'.join(current_content)
                        current_topic['subtopics'].append(current_subtopic)
                    self.hierarchy['topics'].append(current_topic)
                
                current_topic = {
                    'title': text,
                    'page': block.get('page', 1),
                    'subtopics': [],
                    'learning_objectives': [],
                    'key_terms': []
                }
                current_subtopic = None
                current_content = []
                continue
            
            # Detect subtopic (section)
            if block_type in ['section', 'subsection'] or (font_size > avg_font * 1.1 and is_bold):
                if current_topic:
                    if current_subtopic:
                        current_subtopic['content'] = '\n'.join(current_content)
                        current_topic['subtopics'].append(current_subtopic)
                    
                    current_subtopic = {
                        'title': text,
                        'page': block.get('page', 1),
                        'content': ''
                    }
                    current_content = []
                continue
            
            # Regular content
            current_content.append(text)
            
            # Extract learning objectives
            self._extract_learning_objectives(text)
            
            # Extract key terms
            self._extract_key_terms(text)
        
        # Save final topic/subtopic
        if current_topic:
            if current_subtopic:
                current_subtopic['content'] = '\n'.join(current_content)
                current_topic['subtopics'].append(current_subtopic)
            self.hierarchy['topics'].append(current_topic)
        
        # Generate micro-lessons
        self._generate_micro_lessons()
    
    def _extract_learning_objectives(self, text):
        """Extract and classify learning objectives."""
        obj_patterns = [
            r'(?:students?\s*(?:will|should)\s*(?:be\s*able\s*to)?)\s*([^.]+\.)',
            r'(?:learning\s*objectives?[:\s]*)\s*([^.]+\.)',
            r'(?:by\s*the\s*end[^:]*:)\s*([^.]+\.)',
        ]
        
        for pattern in obj_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                objective = match.strip()
                if len(objective) > 15:  # Filter short matches
                    bloom_level = self._classify_bloom_level(objective)
                    
                    self.learning_objectives.append({
                        'objective': objective,
                        'bloom_level': bloom_level,
                        'bloom_description': self.BLOOMS_TAXONOMY[bloom_level]['description'],
                        'cognitive_level': self.BLOOMS_TAXONOMY[bloom_level]['level']
                    })
    
    def _classify_bloom_level(self, text):
        """Classify objective by Bloom's taxonomy level."""
        text_lower = text.lower()
        
        # Check each level from highest to lowest
        for level in ['create', 'evaluate', 'analyze', 'apply', 'understand', 'remember']:
            for verb in self.BLOOMS_TAXONOMY[level]['verbs']:
                if verb in text_lower:
                    return level
        
        return 'understand'  # Default
    
    def _extract_key_terms(self, text):
        """Extract key terms and definitions."""
        # Pattern: Term: Definition or Term - Definition
        patterns = [
            r'([A-Z][a-z]+(?:\s+[A-Z]?[a-z]+)*)\s*[:\-–]\s*([^.]{20,}\.)',
            r'(?:defined\s*as|refers\s*to|means)\s*([^.]+\.)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple) and len(match) >= 2:
                    term, definition = match[0], match[1]
                    if len(term) < 50 and len(definition) > 20:
                        self.key_terms.append({
                            'term': term.strip(),
                            'definition': definition.strip()
                        })
    
    def _generate_micro_lessons(self):
        """Generate micro-learning lessons from structured content."""
        lesson_id = 0
        
        # Get difficulty settings
        difficulty_info = self.DIFFICULTY_MAPPING.get(self.grade_level, {'base': 3, 'words_per_min': 150})
        
        for topic in self.hierarchy['topics']:
            for subtopic in topic.get('subtopics', []):
                content = subtopic.get('content', '')
                if not content or len(content) < 100:
                    continue
                
                # Split content into digestible chunks (~250-300 words)
                words = content.split()
                chunk_size = 250
                chunks = []
                
                for i in range(0, len(words), chunk_size):
                    chunk = ' '.join(words[i:i+chunk_size])
                    if len(chunk) > 50:  # Minimum content
                        chunks.append(chunk)
                
                for idx, chunk in enumerate(chunks):
                    word_count = len(chunk.split())
                    estimated_time = max(2, round(word_count / difficulty_info['words_per_min']))
                    
                    # Calculate difficulty based on content complexity
                    difficulty = self._calculate_difficulty(chunk, difficulty_info['base'])
                    
                    self.micro_lessons.append({
                        'id': f"lesson_{lesson_id}",
                        'topic': topic['title'],
                        'subtopic': subtopic['title'],
                        'title': f"{subtopic['title']}" + (f" - Part {idx + 1}" if len(chunks) > 1 else ""),
                        'content': chunk,
                        'word_count': word_count,
                        'estimated_time_minutes': estimated_time,
                        'difficulty_level': difficulty,
                        'page_reference': subtopic.get('page', topic.get('page', 1)),
                        'status': 'pending_review',
                        'teacher_notes': '',
                        'created_at': datetime.now().isoformat()
                    })
                    lesson_id += 1
    
    def _calculate_difficulty(self, text, base_difficulty):
        """Calculate content difficulty based on various factors."""
        # Factors: sentence length, vocabulary complexity, technical terms
        sentences = text.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        
        # Adjust based on sentence complexity
        if avg_sentence_length > 25:
            base_difficulty += 1
        elif avg_sentence_length < 12:
            base_difficulty -= 1
        
        return max(1, min(5, base_difficulty))  # Clamp between 1-5
    
    def get_structured_output(self):
        """Return complete structured output."""
        return {
            'hierarchy': self.hierarchy,
            'learning_objectives': self.learning_objectives,
            'key_terms': self.key_terms[:30],  # Limit to top 30
            'micro_lessons': self.micro_lessons,
            'tables_figures': self.tables_figures
        }


class PerformanceAdaptationLayer:
    """
    Module 4: Performance Adaptation Layer
    Dynamically adjusts content based on student performance data.
    Personalizes difficulty and depth based on quiz results and engagement.
    """
    
    def __init__(self):
        self.student_profiles = {}
    
    def get_adapted_content(self, student_id, micro_lessons, performance_data=None):
        """Adapt content based on student performance."""
        if not performance_data:
            return micro_lessons  # Return original if no performance data
        
        # Calculate student mastery level
        quiz_scores = performance_data.get('quiz_scores', [])
        engagement = performance_data.get('engagement_score', 50)
        
        avg_score = sum(quiz_scores) / len(quiz_scores) if quiz_scores else 50
        
        adapted_lessons = []
        for lesson in micro_lessons:
            adapted = lesson.copy()
            
            # Adjust based on performance
            if avg_score >= 80:
                # High performer: increase complexity
                adapted['adaptation'] = 'advanced'
                adapted['supplementary'] = 'Consider exploring advanced topics'
            elif avg_score <= 40:
                # Struggling: simplify
                adapted['adaptation'] = 'simplified'
                adapted['supplementary'] = 'Review foundational concepts first'
            else:
                adapted['adaptation'] = 'standard'
            
            adapted_lessons.append(adapted)
        
        return adapted_lessons


class ECESEProcessor:
    """
    Main ECESE Pipeline Processor
    Integrates all modules for complete content extraction and structuring.
    """
    
    def __init__(self, pdf_path, session_id, subject_scope=None, grade_level=None, syllabus_topics=None):
        self.pdf_path = pdf_path
        self.session_id = session_id
        self.subject_scope = subject_scope or []
        self.grade_level = grade_level or ""
        self.syllabus_topics = syllabus_topics or []
        
        # Initialize modules
        self.parsing_unit = ContentParsingUnit(pdf_path)
        self.scope_filter = ScopeFilteringModule(
            scope_keywords=subject_scope,
            syllabus_topics=syllabus_topics,
            grade_level=grade_level
        )
        self.structuring_engine = StructuringEngine(
            subject_name=subject_scope[0] if subject_scope else "General",
            grade_level=grade_level
        )
        self.adaptation_layer = PerformanceAdaptationLayer()
        
        # Processing results
        self.processing_log = []
        self.final_output = None
    
    def process(self):
        """Execute the complete ECESE pipeline."""
        try:
            # Step 1: Content Parsing
            self._log("Starting Content Parsing Unit...")
            if not self.parsing_unit.parse_document():
                self._log("Error: Failed to parse document", "error")
                return False
            
            parsed = self.parsing_unit.get_parsed_content()
            self._log(f"Parsed {len(parsed['raw_blocks'])} content blocks")
            
            # Step 2: Scope Filtering
            self._log("Applying Scope Filtering Module...")
            filtered, flagged, alignment_score = self.scope_filter.filter_content(parsed['raw_blocks'])
            self._log(f"Filtered content: {len(filtered)} aligned, {len(flagged)} flagged ({alignment_score:.1f}% alignment)")
            
            # Step 3: Content Structuring
            self._log("Running Structuring Engine...")
            self.structuring_engine.structure_content(filtered, parsed['metadata'])
            structured = self.structuring_engine.get_structured_output()
            self._log(f"Generated {len(structured['micro_lessons'])} micro-lessons")
            
            # Compile final output
            self.final_output = {
                'metadata': parsed['metadata'],
                'scope_report': self.scope_filter.get_scope_report(),
                'chapters': structured['hierarchy']['topics'],
                'learning_objectives': structured['learning_objectives'],
                'key_terms': structured['key_terms'],
                'micro_lessons': structured['micro_lessons'],
                'processing_log': self.processing_log,
                'flagged_content': flagged[:10]  # First 10 flagged items for review
            }
            
            self._log("ECESE processing complete!", "success")
            return True
            
        except Exception as e:
            self._log(f"Processing error: {str(e)}", "error")
            return False
    
    def _log(self, message, level="info"):
        """Add entry to processing log."""
        self.processing_log.append({
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message
        })
    
    def get_output(self):
        """Get final structured output."""
        return self.final_output
    
    def export_json(self, output_path):
        """Export as JSON."""
        if self.final_output:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.final_output, f, indent=2, ensure_ascii=False)
    
    def export_csv(self, output_path):
        """Export micro-lessons as CSV."""
        if self.final_output and self.final_output.get('micro_lessons'):
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                lessons = self.final_output['micro_lessons']
                if lessons:
                    writer = csv.DictWriter(f, fieldnames=lessons[0].keys())
                    writer.writeheader()
                    writer.writerows(lessons)


# ==================== ROUTES ====================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pdf-extractor')
def pdf_extractor():
    return render_template('pdf_extractor.html')


@app.route('/ecese')
def ecese():
    return render_template('ecese.html')


# PDF Extraction endpoints
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        session_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        session_upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
        os.makedirs(session_upload_dir, exist_ok=True)
        
        file_path = os.path.join(session_upload_dir, filename)
        file.save(file_path)
        
        result = extract_data_from_pdf(file_path, session_id)
        result['session_id'] = session_id
        result['filename'] = filename
        
        return jsonify(result)
    
    return jsonify({'success': False, 'error': 'Invalid file type. Only PDF files are allowed.'}), 400


@app.route('/extracted/<session_id>/images/<filename>')
def serve_image(session_id, filename):
    image_dir = os.path.join(app.config['EXTRACTED_FOLDER'], session_id, 'images')
    return send_from_directory(image_dir, filename)


# ECESE endpoints
@app.route('/ecese/process', methods=['POST'])
def process_ecese():
    """Process educational documents through ECESE pipeline with multi-file support."""
    
    # Check for textbook (required)
    if 'textbook' not in request.files:
        return jsonify({'success': False, 'error': 'No textbook uploaded'}), 400
    
    textbook_file = request.files['textbook']
    teachers_guide_file = request.files.get('teachers_guide')  # Optional
    
    subject_scope = request.form.get('subject_scope', '')
    grade_level = request.form.get('grade_level', '')
    syllabus_topics = request.form.get('syllabus_topics', '')
    
    if textbook_file.filename == '':
        return jsonify({'success': False, 'error': 'No textbook selected'}), 400
    
    if not allowed_file(textbook_file.filename):
        return jsonify({'success': False, 'error': 'Invalid textbook file type. Only PDF allowed.'}), 400
    
    session_id = str(uuid.uuid4())
    session_dir = os.path.join(app.config['ECESE_FOLDER'], session_id)
    os.makedirs(session_dir, exist_ok=True)
    
    # Save textbook
    textbook_filename = secure_filename(textbook_file.filename)
    textbook_path = os.path.join(session_dir, f"textbook_{textbook_filename}")
    textbook_file.save(textbook_path)
    
    # Initialize scope data
    scope_keywords = [s.strip() for s in subject_scope.split(',') if s.strip()]
    syllabus_list = [s.strip() for s in syllabus_topics.split(',') if s.strip()]
    guide_data = None
    
    # Process Teacher's Guide if provided
    if teachers_guide_file and teachers_guide_file.filename:
        if allowed_file(teachers_guide_file.filename):
            guide_filename = secure_filename(teachers_guide_file.filename)
            guide_path = os.path.join(session_dir, f"guide_{guide_filename}")
            teachers_guide_file.save(guide_path)
            
            # Extract scope from teacher's guide
            guide_extractor = TeachersGuideExtractor(guide_path)
            if guide_extractor.extract():
                guide_data = guide_extractor.get_scope_data()
                
                # Merge extracted keywords with manual input
                if guide_data['keywords']:
                    scope_keywords = list(set(scope_keywords + guide_data['keywords']))
                
                if guide_data['topics']:
                    syllabus_list = list(set(syllabus_list + [t.lower() for t in guide_data['topics']]))
    
    # Process textbook through ECESE pipeline
    processor = ECESEProcessor(
        pdf_path=textbook_path,
        session_id=session_id,
        subject_scope=scope_keywords,
        grade_level=grade_level,
        syllabus_topics=syllabus_list
    )
    
    if processor.process():
        result = processor.get_output()
        
        # Add guide extraction info to result
        if guide_data:
            result['teachers_guide_extraction'] = {
                'topics_found': len(guide_data['topics']),
                'keywords_extracted': len(guide_data['keywords']),
                'learning_outcomes': len(guide_data['learning_outcomes']),
                'topics': guide_data['topics'][:20],
                'keywords': guide_data['keywords'][:30]
            }
        
        # Save outputs
        json_path = os.path.join(session_dir, 'structured_content.json')
        processor.export_json(json_path)
        
        csv_path = os.path.join(session_dir, 'micro_lessons.csv')
        processor.export_csv(csv_path)
        
        # ========== AUTO-IMPORT TO MLDC ==========
        mldc_import_result = None
        if MONGO_CONNECTED:
            try:
                mldc_import_result = auto_import_to_mldc(result, session_id, textbook_filename, grade_level)
            except Exception as e:
                print(f"MLDC auto-import error: {e}")
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'filename': textbook_filename,
            'has_teachers_guide': guide_data is not None,
            'data': result,
            'mldc_import': mldc_import_result,
            'exports': {
                'json': f'/ecese/download/{session_id}/json',
                'csv': f'/ecese/download/{session_id}/csv'
            }
        })
    else:
        return jsonify({'success': False, 'error': 'Processing failed'}), 500


def auto_import_to_mldc(content, session_id, filename, grade_level):
    """
    Automatically import ECESE structured content to MLDC.
    Generates quizzes and daily challenges from micro-lessons.
    """
    if not MONGO_CONNECTED or not content:
        return None
    
    # Create course in MongoDB
    course_data = {
        'session_id': session_id,
        'title': content.get('metadata', {}).get('title') or filename.replace('.pdf', ''),
        'filename': filename,
        'grade_level': grade_level,
        'created_at': datetime.now(),
        'micro_lessons': content.get('micro_lessons', []),
        'key_terms': content.get('key_terms', []),
        'learning_objectives': content.get('learning_objectives', []),
        'chapters': content.get('chapters', []),
        'total_lessons': len(content.get('micro_lessons', [])),
        'status': 'active',
        'auto_imported': True
    }
    
    # Insert course
    course_result = db.courses.insert_one(course_data)
    course_id = str(course_result.inserted_id)
    
    # Generate quizzes from content
    quiz_gen = QuizGenerator(content)
    quizzes_created = 0
    challenges_created = 0
    
    # Generate quiz for each micro-lesson
    for lesson in content.get('micro_lessons', []):
        questions = quiz_gen.generate_quiz(lesson_id=lesson.get('id'), num_questions=5)
        
        if questions:
            quiz_data = {
                'course_id': course_id,
                'session_id': session_id,
                'lesson_id': lesson.get('id'),
                'lesson_title': lesson.get('title'),
                'topic': lesson.get('topic', ''),
                'questions': questions,
                'difficulty': lesson.get('difficulty_level', 3),
                'estimated_time': len(questions) * 2,  # 2 min per question
                'created_at': datetime.now(),
                'status': 'approved',  # Auto-approve for immediate use
                'auto_generated': True
            }
            db.quizzes.insert_one(quiz_data)
            quizzes_created += 1
    
    # Generate daily challenges from key terms
    if content.get('key_terms'):
        term_questions = []
        for term in content.get('key_terms', [])[:10]:
            q = quiz_gen._generate_definition_question(term)
            if q:
                term_questions.append(q)
        
        if term_questions:
            challenge_data = {
                'course_id': course_id,
                'session_id': session_id,
                'type': 'daily_challenge',
                'title': f"Key Terms Challenge - {filename.replace('.pdf', '')}",
                'questions': term_questions,
                'difficulty': 2,
                'estimated_time': len(term_questions) * 2,
                'created_at': datetime.now(),
                'status': 'approved',
                'is_daily_challenge': True,
                'auto_generated': True
            }
            db.quizzes.insert_one(challenge_data)
            challenges_created += 1
    
    # Generate mixed challenge from learning objectives
    if content.get('learning_objectives'):
        obj_questions = []
        for obj in content.get('learning_objectives', [])[:5]:
            obj_questions.append({
                'id': str(uuid.uuid4()),
                'type': 'true_false',
                'question': f"Learning Objective: {obj.get('objective', '')}",
                'options': ['I understand this objective', 'I need to review this'],
                'correct_answer': 'I understand this objective',
                'correct_index': 0,
                'difficulty': 2,
                'topic': 'Learning Objectives',
                'bloom_level': obj.get('bloom_level', 'understand'),
                'points': 5
            })
        
        if obj_questions:
            challenge_data = {
                'course_id': course_id,
                'session_id': session_id,
                'type': 'objectives_review',
                'title': f"Learning Objectives Review",
                'questions': obj_questions,
                'difficulty': 2,
                'estimated_time': len(obj_questions),
                'created_at': datetime.now(),
                'status': 'approved',
                'is_daily_challenge': True,
                'auto_generated': True
            }
            db.quizzes.insert_one(challenge_data)
            challenges_created += 1
    
    return {
        'success': True,
        'course_id': course_id,
        'quizzes_created': quizzes_created,
        'challenges_created': challenges_created,
        'total_lessons': len(content.get('micro_lessons', []))
    }


@app.route('/ecese/update-lesson', methods=['POST'])
def update_lesson():
    """Update a micro-lesson (teacher review)."""
    data = request.get_json()
    session_id = data.get('session_id')
    lesson_id = data.get('lesson_id')
    updates = data.get('updates', {})
    
    if not session_id or not lesson_id:
        return jsonify({'success': False, 'error': 'Missing session_id or lesson_id'}), 400
    
    json_path = os.path.join(app.config['ECESE_FOLDER'], session_id, 'structured_content.json')
    
    if not os.path.exists(json_path):
        return jsonify({'success': False, 'error': 'Session not found'}), 404
    
    with open(json_path, 'r', encoding='utf-8') as f:
        content = json.load(f)
    
    # Find and update the lesson
    for lesson in content.get('micro_lessons', []):
        if lesson['id'] == lesson_id:
            lesson.update(updates)
            lesson['last_modified'] = datetime.now().isoformat()
            break
    
    # Save updated content
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2, ensure_ascii=False)
    
    return jsonify({'success': True, 'message': 'Lesson updated'})


@app.route('/ecese/download/<session_id>/<format>')
def download_ecese(session_id, format):
    """Download structured content in various formats."""
    session_dir = os.path.join(app.config['ECESE_FOLDER'], session_id)
    
    if format == 'json':
        return send_from_directory(session_dir, 'structured_content.json', as_attachment=True)
    elif format == 'csv':
        return send_from_directory(session_dir, 'micro_lessons.csv', as_attachment=True)
    else:
        return jsonify({'success': False, 'error': 'Invalid format'}), 400


# ==================== MLDC MODULE ====================
# Micro-Learning via Daily Challenges

class QuizGenerator:
    """
    Task Generator for MLDC
    Generates personalized quizzes from structured content using rule-based logic.
    """
    
    QUESTION_TEMPLATES = {
        'definition': [
            "What is the definition of {term}?",
            "Define {term}.",
            "{term} refers to:",
        ],
        'concept': [
            "Which of the following best describes {concept}?",
            "What is true about {concept}?",
            "{concept} is characterized by:",
        ],
        'application': [
            "How would you apply {concept} in practice?",
            "Which scenario best demonstrates {concept}?",
        ],
        'comparison': [
            "What is the difference between {term1} and {term2}?",
            "Compare and contrast {term1} with {term2}.",
        ],
        'fill_blank': [
            "Complete the following: {sentence_with_blank}",
            "Fill in the blank: {sentence_with_blank}",
        ],
        'true_false': [
            "True or False: {statement}",
        ],
    }
    
    def __init__(self, content_data):
        self.content = content_data
        self.micro_lessons = content_data.get('micro_lessons', [])
        self.key_terms = content_data.get('key_terms', [])
        self.learning_objectives = content_data.get('learning_objectives', [])
    
    def generate_quiz(self, lesson_id=None, difficulty=3, num_questions=5):
        """Generate a quiz from content."""
        questions = []
        
        # Generate from key terms
        for term in self.key_terms[:num_questions]:
            q = self._generate_definition_question(term)
            if q:
                questions.append(q)
        
        # Generate from micro-lessons
        for lesson in self.micro_lessons:
            if lesson_id and lesson['id'] != lesson_id:
                continue
            q = self._generate_content_question(lesson, difficulty)
            if q:
                questions.append(q)
        
        # Shuffle and limit
        random.shuffle(questions)
        return questions[:num_questions]
    
    def _generate_definition_question(self, term_data):
        """Generate a definition-based question."""
        term = term_data.get('term', '')
        definition = term_data.get('definition', '')
        
        if not term or not definition:
            return None
        
        # Create multiple choice options
        wrong_options = self._generate_distractors(definition, 3)
        options = [definition] + wrong_options
        random.shuffle(options)
        
        return {
            'id': str(uuid.uuid4()),
            'type': 'multiple_choice',
            'question': f"What is the definition of '{term}'?",
            'options': options,
            'correct_answer': definition,
            'correct_index': options.index(definition),
            'difficulty': 2,
            'topic': term,
            'bloom_level': 'remember',
            'points': 10
        }
    
    def _generate_content_question(self, lesson, difficulty):
        """Generate a question from lesson content."""
        content = lesson.get('content', '')
        title = lesson.get('title', '')
        
        if len(content) < 50:
            return None
        
        # Extract key sentences
        sentences = content.split('.')
        if not sentences:
            return None
        
        key_sentence = sentences[0].strip()
        if len(key_sentence) < 20:
            key_sentence = sentences[1].strip() if len(sentences) > 1 else key_sentence
        
        # True/False question
        return {
            'id': str(uuid.uuid4()),
            'type': 'true_false',
            'question': f"True or False: {key_sentence}.",
            'options': ['True', 'False'],
            'correct_answer': 'True',
            'correct_index': 0,
            'difficulty': difficulty,
            'topic': title,
            'bloom_level': 'understand',
            'points': 10
        }
    
    def _generate_distractors(self, correct_answer, num=3):
        """Generate plausible wrong answers."""
        distractors = []
        words = correct_answer.split()
        
        # Shuffle words
        if len(words) > 3:
            shuffled = words.copy()
            random.shuffle(shuffled)
            distractors.append(' '.join(shuffled[:len(shuffled)//2]) + '...')
        
        # Generic distractors
        generic = [
            "None of the above",
            "All of the above",
            "This concept is not defined",
            "A combination of multiple factors",
            "The opposite of the stated definition"
        ]
        
        while len(distractors) < num:
            d = random.choice(generic)
            if d not in distractors:
                distractors.append(d)
        
        return distractors[:num]


class AdaptiveScheduler:
    """
    Motivation-aware Delivery Scheduler
    Adjusts task timing based on engagement patterns and performance.
    """
    
    def __init__(self, student_id):
        self.student_id = student_id
        self.performance_history = []
        self.engagement_data = {}
    
    def get_optimal_schedule(self, tasks, student_performance=None):
        """Calculate optimal task schedule using spaced repetition."""
        scheduled_tasks = []
        base_interval = 1  # days
        
        for i, task in enumerate(tasks):
            # Apply spaced repetition intervals
            if student_performance:
                # Adjust based on weakness
                weakness_factor = self._calculate_weakness_factor(task, student_performance)
                interval = base_interval * weakness_factor
            else:
                interval = base_interval * (i + 1)
            
            scheduled_tasks.append({
                'task': task,
                'scheduled_date': (datetime.now() + timedelta(days=interval)).isoformat(),
                'priority': self._calculate_priority(task, student_performance),
                'estimated_time': task.get('estimated_time_minutes', 5)
            })
        
        # Sort by priority
        scheduled_tasks.sort(key=lambda x: x['priority'], reverse=True)
        return scheduled_tasks
    
    def _calculate_weakness_factor(self, task, performance):
        """Calculate weakness factor for a task."""
        topic = task.get('topic', '')
        
        # Check if topic is a weakness
        weak_topics = performance.get('weak_topics', [])
        if topic.lower() in [t.lower() for t in weak_topics]:
            return 0.5  # Schedule sooner
        
        return 1.0
    
    def _calculate_priority(self, task, performance):
        """Calculate task priority."""
        base_priority = 50
        
        # Increase priority for weak areas
        if performance:
            weak_topics = performance.get('weak_topics', [])
            topic = task.get('topic', '')
            if topic.lower() in [t.lower() for t in weak_topics]:
                base_priority += 30
        
        # Increase priority for due tasks
        difficulty = task.get('difficulty_level', 3)
        base_priority += (5 - difficulty) * 5
        
        return min(100, base_priority)


class GamificationEngine:
    """
    Gamification system for MLDC
    Handles streaks, badges, points, and leaderboards.
    """
    
    BADGES = {
        'first_quiz': {'name': 'First Steps', 'description': 'Complete your first quiz', 'icon': '🎯'},
        'streak_3': {'name': 'On Fire', 'description': '3 day streak', 'icon': '🔥'},
        'streak_7': {'name': 'Week Warrior', 'description': '7 day streak', 'icon': '⚡'},
        'streak_30': {'name': 'Monthly Master', 'description': '30 day streak', 'icon': '🏆'},
        'perfect_quiz': {'name': 'Perfect Score', 'description': '100% on a quiz', 'icon': '💯'},
        'quick_learner': {'name': 'Quick Learner', 'description': 'Complete 10 quizzes', 'icon': '📚'},
        'improvement': {'name': 'Rising Star', 'description': 'Improve score by 20%', 'icon': '⭐'},
    }
    
    def __init__(self, student_id):
        self.student_id = student_id
    
    def calculate_streak(self, activity_dates):
        """Calculate current streak."""
        if not activity_dates:
            return 0
        
        sorted_dates = sorted(activity_dates, reverse=True)
        streak = 1
        
        for i in range(1, len(sorted_dates)):
            diff = (sorted_dates[i-1] - sorted_dates[i]).days
            if diff == 1:
                streak += 1
            else:
                break
        
        return streak
    
    def check_badges(self, student_data):
        """Check and award badges."""
        earned_badges = student_data.get('badges', [])
        new_badges = []
        
        # First quiz badge
        if student_data.get('quizzes_completed', 0) >= 1 and 'first_quiz' not in earned_badges:
            new_badges.append('first_quiz')
        
        # Streak badges
        streak = student_data.get('current_streak', 0)
        if streak >= 3 and 'streak_3' not in earned_badges:
            new_badges.append('streak_3')
        if streak >= 7 and 'streak_7' not in earned_badges:
            new_badges.append('streak_7')
        if streak >= 30 and 'streak_30' not in earned_badges:
            new_badges.append('streak_30')
        
        # Perfect score badge
        if student_data.get('perfect_scores', 0) >= 1 and 'perfect_quiz' not in earned_badges:
            new_badges.append('perfect_quiz')
        
        # Quick learner badge
        if student_data.get('quizzes_completed', 0) >= 10 and 'quick_learner' not in earned_badges:
            new_badges.append('quick_learner')
        
        return new_badges
    
    def get_badge_info(self, badge_id):
        """Get badge information."""
        return self.BADGES.get(badge_id, {})


class WeaknessTracker:
    """
    Tracks student weaknesses and generates remedial content.
    """
    
    def __init__(self, student_id):
        self.student_id = student_id
    
    def analyze_performance(self, quiz_results):
        """Analyze quiz results to identify weaknesses."""
        topic_scores = {}
        topic_attempts = {}
        
        for result in quiz_results:
            topic = result.get('topic', 'General')
            score = result.get('score', 0)
            max_score = result.get('max_score', 100)
            
            if topic not in topic_scores:
                topic_scores[topic] = 0
                topic_attempts[topic] = 0
            
            topic_scores[topic] += (score / max_score) * 100
            topic_attempts[topic] += 1
        
        # Calculate average scores per topic
        topic_averages = {}
        for topic in topic_scores:
            topic_averages[topic] = topic_scores[topic] / topic_attempts[topic]
        
        # Identify weak topics (below 60%)
        weak_topics = [topic for topic, avg in topic_averages.items() if avg < 60]
        strong_topics = [topic for topic, avg in topic_averages.items() if avg >= 80]
        
        return {
            'topic_averages': topic_averages,
            'weak_topics': weak_topics,
            'strong_topics': strong_topics,
            'overall_average': sum(topic_averages.values()) / len(topic_averages) if topic_averages else 0
        }
    
    def generate_remedial_tasks(self, weak_topics, available_content):
        """Generate remedial tasks for weak areas."""
        remedial_tasks = []
        
        for topic in weak_topics:
            # Find related content
            for lesson in available_content.get('micro_lessons', []):
                if topic.lower() in lesson.get('topic', '').lower() or topic.lower() in lesson.get('title', '').lower():
                    remedial_tasks.append({
                        'type': 'review',
                        'lesson_id': lesson.get('id'),
                        'title': f"Review: {lesson.get('title')}",
                        'priority': 'high',
                        'estimated_time': lesson.get('estimated_time_minutes', 5)
                    })
        
        return remedial_tasks


# ==================== MLDC ROUTES ====================

@app.route('/mldc')
def mldc():
    """Micro-Learning Daily Challenges page."""
    return render_template('mldc.html')


@app.route('/mldc/import-content', methods=['POST'])
def import_content_to_mldc():
    """Import structured content from ECESE to MLDC."""
    if not MONGO_CONNECTED:
        return jsonify({'success': False, 'error': 'Database not connected'}), 500
    
    data = request.get_json()
    session_id = data.get('session_id')
    
    if not session_id:
        return jsonify({'success': False, 'error': 'Session ID required'}), 400
    
    # Load ECESE content
    json_path = os.path.join(app.config['ECESE_FOLDER'], session_id, 'structured_content.json')
    
    if not os.path.exists(json_path):
        return jsonify({'success': False, 'error': 'Content not found'}), 404
    
    with open(json_path, 'r', encoding='utf-8') as f:
        content = json.load(f)
    
    # Generate quizzes from content
    quiz_gen = QuizGenerator(content)
    
    # Create course in MongoDB
    course_data = {
        'session_id': session_id,
        'title': content.get('metadata', {}).get('title', 'Imported Course'),
        'created_at': datetime.now(),
        'micro_lessons': content.get('micro_lessons', []),
        'key_terms': content.get('key_terms', []),
        'learning_objectives': content.get('learning_objectives', []),
        'chapters': content.get('chapters', []),
        'total_lessons': len(content.get('micro_lessons', [])),
        'status': 'active'
    }
    
    # Insert into MongoDB
    result = db.courses.insert_one(course_data)
    course_id = str(result.inserted_id)
    
    # Generate initial quiz bank
    quizzes = []
    for lesson in content.get('micro_lessons', []):
        quiz = quiz_gen.generate_quiz(lesson_id=lesson.get('id'), num_questions=3)
        if quiz:
            quiz_data = {
                'course_id': course_id,
                'lesson_id': lesson.get('id'),
                'lesson_title': lesson.get('title'),
                'questions': quiz,
                'created_at': datetime.now(),
                'status': 'pending_review'  # Teacher needs to review
            }
            quizzes.append(quiz_data)
    
    if quizzes:
        db.quizzes.insert_many(quizzes)
    
    return jsonify({
        'success': True,
        'course_id': course_id,
        'lessons_imported': len(content.get('micro_lessons', [])),
        'quizzes_generated': len(quizzes)
    })


@app.route('/mldc/courses', methods=['GET'])
def get_mldc_courses():
    """Get all imported courses."""
    if not MONGO_CONNECTED:
        return jsonify({'success': False, 'error': 'Database not connected'}), 500
    
    courses = list(db.courses.find({}, {'micro_lessons': 0}).sort('created_at', -1))
    
    # Convert ObjectId to string
    for course in courses:
        course['_id'] = str(course['_id'])
        course['created_at'] = course['created_at'].isoformat() if course.get('created_at') else None
    
    return jsonify({'success': True, 'courses': courses})


@app.route('/mldc/course/<course_id>', methods=['GET'])
def get_course_details(course_id):
    """Get course details with lessons."""
    if not MONGO_CONNECTED:
        return jsonify({'success': False, 'error': 'Database not connected'}), 500
    
    course = db.courses.find_one({'_id': ObjectId(course_id)})
    if not course:
        return jsonify({'success': False, 'error': 'Course not found'}), 404
    
    course['_id'] = str(course['_id'])
    course['created_at'] = course['created_at'].isoformat() if course.get('created_at') else None
    
    # Get quizzes for this course
    quizzes = list(db.quizzes.find({'course_id': course_id}))
    for quiz in quizzes:
        quiz['_id'] = str(quiz['_id'])
        quiz['created_at'] = quiz['created_at'].isoformat() if quiz.get('created_at') else None
    
    return jsonify({'success': True, 'course': course, 'quizzes': quizzes})


@app.route('/mldc/daily-challenge', methods=['GET'])
def get_daily_challenge():
    """Get today's daily challenge."""
    if not MONGO_CONNECTED:
        return jsonify({'success': False, 'error': 'Database not connected'}), 500
    
    student_id = request.args.get('student_id', 'default_student')
    
    # Get or create student profile
    student = db.students.find_one({'student_id': student_id})
    if not student:
        student = {
            'student_id': student_id,
            'created_at': datetime.now(),
            'total_points': 0,
            'current_streak': 0,
            'badges': [],
            'quizzes_completed': 0,
            'perfect_scores': 0,
            'last_activity': None
        }
        db.students.insert_one(student)
    
    # First try to get daily challenges (prioritize is_daily_challenge = True)
    daily_challenges = list(db.quizzes.find({
        'status': 'approved',
        'is_daily_challenge': True
    }).sort('created_at', -1).limit(10))
    
    # Fallback to regular quizzes if no daily challenges
    if daily_challenges:
        quizzes = daily_challenges
    else:
        quizzes = list(db.quizzes.find({'status': 'approved'}).sort('created_at', -1).limit(10))
    
    if not quizzes:
        # Get any quizzes if no approved ones
        quizzes = list(db.quizzes.find({}).sort('created_at', -1).limit(5))
    
    if not quizzes:
        return jsonify({'success': True, 'challenge': None, 'message': 'No challenges available. Process content in ECESE to auto-generate quizzes!'})
    
    # Select quiz - prefer recently created ones for better engagement
    # Use weighted random: most recent has higher chance
    weights = [1.0 / (i + 1) for i in range(len(quizzes))]
    total_weight = sum(weights)
    normalized_weights = [w / total_weight for w in weights]
    selected_quiz = random.choices(quizzes, weights=normalized_weights, k=1)[0]
    selected_quiz['_id'] = str(selected_quiz['_id'])
    selected_quiz['created_at'] = selected_quiz['created_at'].isoformat() if selected_quiz.get('created_at') else None
    
    # Get student stats
    gamification = GamificationEngine(student_id)
    student['_id'] = str(student['_id']) if student.get('_id') else None
    student['created_at'] = student['created_at'].isoformat() if student.get('created_at') else None
    student['last_activity'] = student['last_activity'].isoformat() if student.get('last_activity') else None
    
    return jsonify({
        'success': True,
        'challenge': selected_quiz,
        'student': student
    })


@app.route('/mldc/submit-quiz', methods=['POST'])
def submit_quiz():
    """Submit quiz answers and calculate score."""
    if not MONGO_CONNECTED:
        return jsonify({'success': False, 'error': 'Database not connected'}), 500
    
    data = request.get_json()
    student_id = data.get('student_id', 'default_student')
    quiz_id = data.get('quiz_id')
    answers = data.get('answers', {})  # {question_id: selected_index}
    
    # Get quiz
    quiz = db.quizzes.find_one({'_id': ObjectId(quiz_id)})
    if not quiz:
        return jsonify({'success': False, 'error': 'Quiz not found'}), 404
    
    # Calculate score
    correct = 0
    total = len(quiz.get('questions', []))
    results = []
    
    for question in quiz.get('questions', []):
        q_id = question.get('id')
        selected = answers.get(q_id)
        is_correct = selected == question.get('correct_index')
        
        if is_correct:
            correct += 1
        
        results.append({
            'question_id': q_id,
            'selected': selected,
            'correct_index': question.get('correct_index'),
            'is_correct': is_correct,
            'points': question.get('points', 10) if is_correct else 0
        })
    
    score = (correct / total * 100) if total > 0 else 0
    points_earned = sum(r['points'] for r in results)
    
    # Update student profile
    student = db.students.find_one({'student_id': student_id})
    if student:
        update_data = {
            '$inc': {
                'total_points': points_earned,
                'quizzes_completed': 1
            },
            '$set': {
                'last_activity': datetime.now()
            }
        }
        
        # Check for perfect score
        if score == 100:
            update_data['$inc']['perfect_scores'] = 1
        
        # Update streak
        if student.get('last_activity'):
            last_activity = student['last_activity']
            if isinstance(last_activity, str):
                last_activity = datetime.fromisoformat(last_activity)
            days_since = (datetime.now() - last_activity).days
            
            if days_since <= 1:
                update_data['$inc']['current_streak'] = 1
            else:
                update_data['$set']['current_streak'] = 1
        else:
            update_data['$set']['current_streak'] = 1
        
        db.students.update_one({'student_id': student_id}, update_data)
        
        # Check for new badges
        updated_student = db.students.find_one({'student_id': student_id})
        gamification = GamificationEngine(student_id)
        new_badges = gamification.check_badges(updated_student)
        
        if new_badges:
            db.students.update_one(
                {'student_id': student_id},
                {'$push': {'badges': {'$each': new_badges}}}
            )
    
    # Save quiz result
    result_data = {
        'student_id': student_id,
        'quiz_id': quiz_id,
        'score': score,
        'correct': correct,
        'total': total,
        'points_earned': points_earned,
        'results': results,
        'submitted_at': datetime.now(),
        'topic': quiz.get('lesson_title', 'General')
    }
    db.quiz_results.insert_one(result_data)
    
    return jsonify({
        'success': True,
        'score': score,
        'correct': correct,
        'total': total,
        'points_earned': points_earned,
        'results': results,
        'new_badges': new_badges if 'new_badges' in dir() else []
    })


@app.route('/mldc/student-stats', methods=['GET'])
def get_student_stats():
    """Get student statistics and analytics."""
    if not MONGO_CONNECTED:
        return jsonify({'success': False, 'error': 'Database not connected'}), 500
    
    student_id = request.args.get('student_id', 'default_student')
    
    # Get student profile
    student = db.students.find_one({'student_id': student_id})
    if not student:
        return jsonify({'success': False, 'error': 'Student not found'}), 404
    
    student['_id'] = str(student['_id'])
    student['created_at'] = student['created_at'].isoformat() if student.get('created_at') else None
    student['last_activity'] = student['last_activity'].isoformat() if student.get('last_activity') else None
    
    # Get quiz results
    results = list(db.quiz_results.find({'student_id': student_id}).sort('submitted_at', -1).limit(20))
    for r in results:
        r['_id'] = str(r['_id'])
        r['submitted_at'] = r['submitted_at'].isoformat() if r.get('submitted_at') else None
    
    # Analyze weaknesses
    tracker = WeaknessTracker(student_id)
    analysis = tracker.analyze_performance(results)
    
    # Get badges info
    gamification = GamificationEngine(student_id)
    badges_info = [gamification.get_badge_info(b) for b in student.get('badges', [])]
    
    return jsonify({
        'success': True,
        'student': student,
        'recent_results': results,
        'analysis': analysis,
        'badges': badges_info
    })


@app.route('/mldc/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get leaderboard."""
    if not MONGO_CONNECTED:
        return jsonify({'success': False, 'error': 'Database not connected'}), 500
    
    # Get top students by points
    students = list(db.students.find({}).sort('total_points', -1).limit(10))
    
    leaderboard = []
    for i, student in enumerate(students):
        leaderboard.append({
            'rank': i + 1,
            'student_id': student.get('student_id'),
            'total_points': student.get('total_points', 0),
            'current_streak': student.get('current_streak', 0),
            'quizzes_completed': student.get('quizzes_completed', 0),
            'badges_count': len(student.get('badges', []))
        })
    
    return jsonify({'success': True, 'leaderboard': leaderboard})


@app.route('/mldc/teacher/review-quizzes', methods=['GET'])
def get_quizzes_for_review():
    """Get quizzes pending teacher review."""
    if not MONGO_CONNECTED:
        return jsonify({'success': False, 'error': 'Database not connected'}), 500
    
    quizzes = list(db.quizzes.find({'status': 'pending_review'}))
    
    for quiz in quizzes:
        quiz['_id'] = str(quiz['_id'])
        quiz['created_at'] = quiz['created_at'].isoformat() if quiz.get('created_at') else None
    
    return jsonify({'success': True, 'quizzes': quizzes})


@app.route('/mldc/teacher/approve-quiz', methods=['POST'])
def approve_quiz():
    """Approve or reject a quiz."""
    if not MONGO_CONNECTED:
        return jsonify({'success': False, 'error': 'Database not connected'}), 500
    
    data = request.get_json()
    quiz_id = data.get('quiz_id')
    action = data.get('action')  # 'approve' or 'reject'
    
    if action not in ['approve', 'reject']:
        return jsonify({'success': False, 'error': 'Invalid action'}), 400
    
    status = 'approved' if action == 'approve' else 'rejected'
    
    db.quizzes.update_one(
        {'_id': ObjectId(quiz_id)},
        {'$set': {'status': status, 'reviewed_at': datetime.now()}}
    )
    
    return jsonify({'success': True, 'status': status})


@app.route('/mldc/ecese-sessions', methods=['GET'])
def get_ecese_sessions():
    """Get available ECESE sessions for import."""
    sessions = []
    
    ecese_folder = app.config['ECESE_FOLDER']
    if os.path.exists(ecese_folder):
        for session_id in os.listdir(ecese_folder):
            json_path = os.path.join(ecese_folder, session_id, 'structured_content.json')
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    content = json.load(f)
                
                sessions.append({
                    'session_id': session_id,
                    'title': content.get('metadata', {}).get('title', 'Untitled'),
                    'lessons_count': len(content.get('micro_lessons', [])),
                    'terms_count': len(content.get('key_terms', []))
                })
    
    return jsonify({'success': True, 'sessions': sessions})


@app.route('/mldc/all-quizzes', methods=['GET'])
def get_all_quizzes():
    """Get all available quizzes for the MLDC module."""
    if not MONGO_CONNECTED:
        return jsonify({'success': False, 'error': 'Database not connected', 'quizzes': []})
    
    try:
        quizzes = list(db.quizzes.find(
            {'status': 'approved'},
            {
                '_id': 1,
                'lesson_title': 1,
                'title': 1,
                'topic': 1,
                'questions': 1,
                'difficulty': 1,
                'estimated_time': 1,
                'is_daily_challenge': 1,
                'status': 1,
                'auto_generated': 1,
                'created_at': 1
            }
        ).sort('created_at', -1).limit(50))
        
        # Convert ObjectId to string
        for quiz in quizzes:
            quiz['_id'] = str(quiz['_id'])
            quiz['questions'] = quiz.get('questions', [])
        
        return jsonify({'success': True, 'quizzes': quizzes})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'quizzes': []})


@app.route('/mldc/quiz/<quiz_id>', methods=['GET'])
def get_specific_quiz(quiz_id):
    """Get a specific quiz by ID."""
    if not MONGO_CONNECTED:
        return jsonify({'success': False, 'error': 'Database not connected'})
    
    try:
        from bson.objectid import ObjectId
        quiz = db.quizzes.find_one({'_id': ObjectId(quiz_id)})
        
        if quiz:
            quiz['_id'] = str(quiz['_id'])
            return jsonify({'success': True, 'quiz': quiz})
        else:
            return jsonify({'success': False, 'error': 'Quiz not found'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
