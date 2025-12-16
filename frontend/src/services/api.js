/**
 * API service module
 * Handles all API calls to the backend
 */
import axios from 'axios';

// Base URL for the backend API
const API_BASE_URL = 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

/**
 * Student API functions
 */
export const studentAPI = {
  // Login student
  login: async (email, password) => {
    // Using POST with request body for better security
    const response = await api.post('/api/students/login', {
      email,
      password,
    });
    return response.data;
  },

  // Get student by ID
  getStudent: async (studentId) => {
    const response = await api.get(`/api/students/${studentId}`);
    return response.data;
  },

  // Get all students
  getAllStudents: async () => {
    const response = await api.get('/api/students/');
    return response.data;
  },
};

/**
 * Pathway API functions
 */
export const pathwayAPI = {
  // Get all pathways
  getAllPathways: async () => {
    const response = await api.get('/api/pathways/');
    return response.data;
  },

  // Get pathway by ID
  getPathway: async (pathwayId) => {
    const response = await api.get(`/api/pathways/${pathwayId}`);
    return response.data;
  },

  // Get pathways by level
  getPathwaysByLevel: async (level) => {
    const response = await api.get(`/api/pathways/level/${level}`);
    return response.data;
  },
};

/**
 * Quiz API functions
 */
export const quizAPI = {
  // Get all quizzes
  getAllQuizzes: async () => {
    const response = await api.get('/api/quizzes/');
    return response.data;
  },

  // Get quiz by ID
  getQuiz: async (quizId) => {
    const response = await api.get(`/api/quizzes/${quizId}`);
    return response.data;
  },

  // Get quizzes by pathway
  getQuizzesByPathway: async (pathwayId) => {
    const response = await api.get(`/api/quizzes/pathway/${pathwayId}`);
    return response.data;
  },
};

/**
 * Results API functions
 */
export const resultsAPI = {
  // Submit quiz answers
  submitQuiz: async (submission) => {
    const response = await api.post('/api/results/submit', submission);
    return response.data;
  },

  // Get student results
  getStudentResults: async (studentId) => {
    const response = await api.get(`/api/results/student/${studentId}`);
    return response.data;
  },

  // Get quiz result for student (optionally after a specific date)
  getQuizResult: async (quizId, studentId, afterDate = null) => {
    let url = `/api/results/quiz/${quizId}/student/${studentId}`;
    if (afterDate) {
      url += `?after_date=${encodeURIComponent(afterDate)}`;
    }
    const response = await api.get(url);
    return response.data;
  },

  // Delete a quiz result
  deleteResult: async (resultId, studentId) => {
    const response = await api.delete(`/api/results/result/${resultId}/student/${studentId}`);
    return response.data;
  },
};

/**
 * Adaptive Learning API functions
 */
export const adaptiveAPI = {
  // Get student concept mastery
  getMastery: async (studentId) => {
    const response = await api.get(`/api/adaptive/mastery/${studentId}`);
    return response.data;
  },

  // Get weak areas
  getWeakAreas: async (studentId, threshold = 0.6) => {
    const response = await api.get(`/api/adaptive/weak-areas/${studentId}?threshold=${threshold}`);
    return response.data;
  },

  // Get recommendations
  getRecommendations: async (studentId, regenerate = false) => {
    const response = await api.get(`/api/adaptive/recommendations/${studentId}?regenerate=${regenerate}`);
    return response.data;
  },

  // Get learning analytics
  getAnalytics: async (studentId) => {
    const response = await api.get(`/api/adaptive/analytics/${studentId}`);
    return response.data;
  },

  // Adjust pathway
  adjustPathway: async (studentId) => {
    const response = await api.post(`/api/adaptive/adjust-pathway/${studentId}`);
    return response.data;
  },
};

/**
 * Authentication API functions
 */
export const authAPI = {
  // Student login
  studentLogin: async (email, password) => {
    const response = await api.post('/api/auth/student/login', {
      email,
      password,
    });
    return response.data;
  },

  // Teacher login
  teacherLogin: async (email, password) => {
    const response = await api.post('/api/auth/teacher/login', {
      email,
      password,
    });
    return response.data;
  },

  // Admin login
  adminLogin: async (email, password) => {
    const response = await api.post('/api/auth/admin/login', {
      email,
      password,
    });
    return response.data;
  },
};

/**
 * Teacher API functions
 */
export const teacherAPI = {
  // Login teacher (legacy - use authAPI.teacherLogin)
  login: async (email, password) => {
    const response = await api.post('/api/auth/teacher/login', {
      email,
      password,
    });
    return response.data;
  },

  // Get teacher by ID
  getTeacher: async (teacherId) => {
    const response = await api.get(`/api/teachers/${teacherId}`);
    return response.data;
  },

  // Get all teachers
  getAllTeachers: async () => {
    const response = await api.get('/api/teachers/');
    return response.data;
  },

  // Get all students progress
  getAllStudentsProgress: async () => {
    const response = await api.get('/api/teachers/students/progress');
    return response.data;
  },

  // Get specific student progress
  getStudentProgress: async (studentId) => {
    const response = await api.get(`/api/teachers/students/${studentId}/progress`);
    return response.data;
  },
};

/**
 * Tasks API functions
 */
export const tasksAPI = {
  // Assign tasks to students
  assignTasks: async (taskData) => {
    const response = await api.post('/api/tasks/assign', taskData);
    return response.data;
  },

  // Get all tasks for a student
  getStudentTasks: async (studentId) => {
    const response = await api.get(`/api/tasks/student/${studentId}`);
    return response.data;
  },

  // Get pending tasks for a student
  getPendingTasks: async (studentId) => {
    const response = await api.get(`/api/tasks/student/${studentId}/pending`);
    return response.data;
  },

  // Update task status
  updateTaskStatus: async (taskId, status) => {
    const response = await api.put(`/api/tasks/${taskId}/status?status=${status}`);
    return response.data;
  },

  // Delete task (teacher only)
  deleteTask: async (taskId) => {
    const response = await api.delete(`/api/tasks/${taskId}`);
    return response.data;
  },
};

/**
 * Analytics API functions
 */
export const analyticsAPI = {
  // Get pathway distribution for pie chart
  getPathwayDistribution: async () => {
    const response = await api.get('/api/analytics/pathway-distribution');
    return response.data;
  },

  // Get students per pathway for bar chart
  getStudentsPerPathway: async () => {
    const response = await api.get('/api/analytics/students-per-pathway');
    return response.data;
  },

  // Get student quiz history for line chart
  getStudentQuizHistory: async (studentId) => {
    const response = await api.get(`/api/analytics/student/${studentId}/quiz-history`);
    return response.data;
  },

  // Get all students summary for teacher
  getStudentsSummary: async () => {
    const response = await api.get('/api/analytics/teacher/students-summary');
    return response.data;
  },

  // Get detailed student information
  getStudentDetails: async (studentId) => {
    const response = await api.get(`/api/analytics/teacher/student/${studentId}/details`);
    return response.data;
  },
};

/**
 * Roadmap API functions
 */
export const roadmapAPI = {
  // Template Management (Teacher)
  createTemplate: async (templateData, teacherId) => {
    const response = await api.post(`/api/roadmap/templates?teacher_id=${teacherId}`, templateData);
    return response.data;
  },

  getAllTemplates: async (filters = {}) => {
    const params = new URLSearchParams(filters).toString();
    const response = await api.get(`/api/roadmap/templates?${params}`);
    return response.data;
  },

  getTemplate: async (templateId) => {
    const response = await api.get(`/api/roadmap/templates/${templateId}`);
    return response.data;
  },

  updateTemplate: async (templateId, updateData, teacherId) => {
    const response = await api.put(`/api/roadmap/templates/${templateId}?teacher_id=${teacherId}`, updateData);
    return response.data;
  },

  deleteTemplate: async (templateId, teacherId) => {
    const response = await api.delete(`/api/roadmap/templates/${templateId}?teacher_id=${teacherId}`);
    return response.data;
  },

  // Roadmap Generation (Student)
  generateRoadmap: async (studentId, options = {}) => {
    const response = await api.post('/api/roadmap/generate', {
      student_id: studentId,
      regenerate: options.regenerate || false,
      focus_areas: options.focus_areas || null,
      template_ids: options.template_ids || null,
      max_tasks: options.max_tasks || null,
      approval_required: options.approval_required || false
    });
    return response.data;
  },

  getStudentRoadmaps: async (studentId, status = null) => {
    const params = status ? `?status=${status}` : '';
    const response = await api.get(`/api/roadmap/student/${studentId}${params}`);
    return response.data;
  },

  getActiveRoadmap: async (studentId) => {
    const response = await api.get(`/api/roadmap/student/${studentId}/active`);
    return response.data;
  },

  updateRoadmapStatus: async (roadmapId, status, teacherId = null) => {
    const params = teacherId ? `?status=${status}&teacher_id=${teacherId}` : `?status=${status}`;
    const response = await api.put(`/api/roadmap/roadmap/${roadmapId}/status${params}`);
    return response.data;
  },

  markTaskComplete: async (roadmapId, taskId) => {
    const response = await api.put(`/api/roadmap/roadmap/${roadmapId}/task/${taskId}/complete`);
    return response.data;
  },

  // Teacher Dashboard
  getStudentRoadmapsForTeacher: async (teacherId, status = null) => {
    const params = status ? `?status=${status}` : '';
    const response = await api.get(`/api/roadmap/teacher/${teacherId}/student-roadmaps${params}`);
    return response.data;
  },
};

// Add token to requests automatically
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
