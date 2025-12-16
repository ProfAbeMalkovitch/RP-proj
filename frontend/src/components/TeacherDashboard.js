/**
 * Teacher Dashboard Component
 * Displays analytics with multiple graphs, student progress, pathway generator, and task assignment
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { analyticsAPI, pathwayAPI, teacherAPI, tasksAPI, quizAPI } from '../services/api';
import { 
  PieChart, Pie, Cell, BarChart, Bar, LineChart, Line, AreaChart, Area,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis
} from 'recharts';
import StudentDetailModal from './StudentDetailModal';
import PathwayBadge from './shared/PathwayBadge';
import SideNavigation from './shared/SideNavigation';
import './TeacherDashboard.css';

const COLORS = {
  Basic: '#FFC107',
  Intermediate: '#17A2B8',
  Accelerated: '#28A745'
};

function TeacherDashboard({ teacher, onLogout }) {
  const [students, setStudents] = useState([]);
  const [pathwayDistribution, setPathwayDistribution] = useState([]);
  const [studentsPerPathway, setStudentsPerPathway] = useState([]);
  const [scoreDistribution, setScoreDistribution] = useState([]);
  const [performanceTrend, setPerformanceTrend] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [showPathwayGenerator, setShowPathwayGenerator] = useState(false);
  const [showTaskAssignment, setShowTaskAssignment] = useState(false);
  const [selectedStudents, setSelectedStudents] = useState([]);
  const [taskForm, setTaskForm] = useState({ title: '', description: '', dueDate: '', quizId: '' });
  const [availableQuizzes, setAvailableQuizzes] = useState([]);
  const [pathwayForm, setPathwayForm] = useState({ studentId: '', pathway: 'Basic' });
  const [searchQuery, setSearchQuery] = useState('');
  const [filteredStudents, setFilteredStudents] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError('');
      
      // Check if token exists
      const token = localStorage.getItem('token');
      if (!token) {
        setError('Authentication required. Please login again.');
        navigate('/login');
        return;
      }
      
      // Fetch all data in parallel
      const [summary, distribution, pathwayData] = await Promise.all([
        analyticsAPI.getStudentsSummary().catch(err => {
          console.error('Error fetching students summary:', err);
          throw new Error(`Students summary: ${err.response?.data?.detail || err.message}`);
        }),
        analyticsAPI.getPathwayDistribution().catch(err => {
          console.error('Error fetching pathway distribution:', err);
          throw new Error(`Pathway distribution: ${err.response?.data?.detail || err.message}`);
        }),
        analyticsAPI.getStudentsPerPathway().catch(err => {
          console.error('Error fetching students per pathway:', err);
          throw new Error(`Students per pathway: ${err.response?.data?.detail || err.message}`);
        })
      ]);
      
      // Validate and set data
      const validSummary = Array.isArray(summary) ? summary : [];
      const validDistribution = Array.isArray(distribution) ? distribution : [];
      const validPathwayData = Array.isArray(pathwayData) ? pathwayData : [];
      
      setStudents(validSummary);
      setFilteredStudents(validSummary);
      setPathwayDistribution(validDistribution);
      setStudentsPerPathway(validPathwayData);
      
      // Generate additional analytics only if we have data
      if (validSummary.length > 0) {
        generateScoreDistribution(validSummary);
        generatePerformanceTrend(validSummary);
      } else {
        // Set empty arrays for charts
        setScoreDistribution([]);
        setPerformanceTrend([]);
      }
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to load dashboard data. Please try again.';
      setError(`Error: ${errorMessage}. Please check your authentication and try again.`);
      console.error('Error fetching dashboard data:', err);
      console.error('Error details:', {
        message: err.message,
        response: err.response?.data,
        status: err.response?.status
      });
    } finally {
      setLoading(false);
    }
  };

  const generateScoreDistribution = (studentsData) => {
    const ranges = [
      { range: '90-100', min: 90, max: 100, count: 0 },
      { range: '80-89', min: 80, max: 89, count: 0 },
      { range: '70-79', min: 70, max: 79, count: 0 },
      { range: '60-69', min: 60, max: 69, count: 0 },
      { range: '0-59', min: 0, max: 59, count: 0 }
    ];
    
    studentsData.forEach(student => {
      const score = student.average_score;
      const range = ranges.find(r => score >= r.min && score <= r.max);
      if (range) range.count++;
    });
    
    setScoreDistribution(ranges);
  };

  const generatePerformanceTrend = (studentsData) => {
    const trendData = [];
    studentsData.forEach(student => {
      if (student.quiz_scores && student.quiz_scores.length >= 2) {
        const recent = student.quiz_scores.slice(-3);
        const earlier = student.quiz_scores.slice(0, Math.max(1, student.quiz_scores.length - 3));
        const recentAvg = recent.reduce((a, b) => a + b, 0) / recent.length;
        const earlierAvg = earlier.reduce((a, b) => a + b, 0) / earlier.length;
        trendData.push({
          name: student.name,
          earlier: earlierAvg.toFixed(1),
          recent: recentAvg.toFixed(1),
          improvement: (recentAvg - earlierAvg).toFixed(1)
        });
      }
    });
    setPerformanceTrend(trendData.slice(0, 10)); // Top 10 for readability
  };

  const handleStudentClick = async (student) => {
    try {
      const details = await analyticsAPI.getStudentDetails(student.student_id);
      setSelectedStudent(details);
      setShowModal(true);
    } catch (err) {
      console.error('Error fetching student details:', err);
      alert('Failed to load student details. Please try again.');
    }
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setSelectedStudent(null);
  };

  const handleStudentSelect = (studentId) => {
    setSelectedStudents(prev => 
      prev.includes(studentId) 
        ? prev.filter(id => id !== studentId)
        : [...prev, studentId]
    );
  };

  const fetchQuizzes = async () => {
    try {
      const quizzes = await quizAPI.getAllQuizzes();
      setAvailableQuizzes(quizzes || []);
    } catch (err) {
      console.error('Error fetching quizzes:', err);
      setAvailableQuizzes([]);
    }
  };

  const handleAssignTask = async (e) => {
    e.preventDefault();
    if (selectedStudents.length === 0) {
      alert('Please select at least one student');
      return;
    }
    
    try {
      // Handle default quiz selection
      let quizIdToUse = null;
      if (taskForm.quizId === 'default') {
        // Auto-select default quiz based on student pathways
        // For multiple students, we'll use the most common pathway or first student's pathway
        const selectedStudentsData = students.filter(s => selectedStudents.includes(s.student_id));
        if (selectedStudentsData.length > 0) {
          // Get pathway distribution
          const pathwayCounts = {};
          selectedStudentsData.forEach(s => {
            const pathway = s.pathway || 'Basic';
            pathwayCounts[pathway] = (pathwayCounts[pathway] || 0) + 1;
          });
          // Get most common pathway
          const mostCommonPathway = Object.keys(pathwayCounts).reduce((a, b) => 
            pathwayCounts[a] > pathwayCounts[b] ? a : b
          );
          
          // Find matching quiz
          const pathwayName = mostCommonPathway.toLowerCase();
          const defaultQuiz = availableQuizzes.find(q => {
            const quizPathway = (q.pathway_id || '').toLowerCase();
            return quizPathway.includes(pathwayName) || 
                   quizPathway.includes('basic') && pathwayName === 'basic' ||
                   quizPathway.includes('intermediate') && pathwayName === 'intermediate' ||
                   quizPathway.includes('accelerated') && pathwayName === 'accelerated';
          });
          
          if (defaultQuiz) {
            quizIdToUse = defaultQuiz.quiz_id;
          }
        }
      } else if (taskForm.quizId) {
        quizIdToUse = taskForm.quizId;
      }
      
      const taskData = {
        student_ids: selectedStudents,
        title: taskForm.title,
        description: taskForm.description,
        due_date: taskForm.dueDate,
        quiz_id: quizIdToUse
      };
      
      const result = await tasksAPI.assignTasks(taskData);
      alert(`✅ ${result.message}`);
      setTaskForm({ title: '', description: '', dueDate: '', quizId: '' });
      setSelectedStudents([]);
      setShowTaskAssignment(false);
    } catch (err) {
      console.error('Error assigning task:', err);
      alert(`Failed to assign task: ${err.response?.data?.detail || err.message}`);
    }
  };

  const handleGeneratePathway = async (e) => {
    e.preventDefault();
    // TODO: Implement pathway generation API call
    alert(`Pathway "${pathwayForm.pathway}" assigned to student`);
    setPathwayForm({ studentId: '', pathway: 'Basic' });
    setShowPathwayGenerator(false);
  };

  const handleSearch = (query) => {
    setSearchQuery(query);
    if (query.trim() === '') {
      setFilteredStudents(students);
    } else {
      const filtered = students.filter(student => 
        student.name.toLowerCase().includes(query.toLowerCase()) ||
        student.email.toLowerCase().includes(query.toLowerCase()) ||
        (student.pathway && student.pathway.toLowerCase().includes(query.toLowerCase()))
      );
      setFilteredStudents(filtered);
    }
  };

  useEffect(() => {
    if (searchQuery.trim() === '') {
      setFilteredStudents(students);
    }
  }, [students, searchQuery]);

  const getPerformanceColor = (score) => {
    if (score >= 80) return '#28a745';
    if (score >= 70) return '#17a2b8';
    if (score >= 50) return '#ffc107';
    return '#dc3545';
  };

  if (loading) {
    return (
      <div className="teacher-dashboard-container">
        <div className="loading">Loading dashboard...</div>
      </div>
    );
  }

  return (
    <div className="teacher-dashboard-container">
      <SideNavigation 
        user={teacher} 
        userRole="teacher" 
        onLogout={onLogout}
        onSearch={handleSearch}
        searchPlaceholder="Search students..."
        onGeneratePathway={() => setShowPathwayGenerator(true)}
        onAssignTasks={() => setShowTaskAssignment(true)}
      />
      
      <div className="dashboard-content">
      <header className="teacher-dashboard-header">
        <div className="header-content">
          <h1>Teacher Dashboard</h1>
        </div>
      </header>

      {error && <div className="error-banner">{error}</div>}

      {/* Statistics Cards */}
      <div className="dashboard-stats">
        <div className="stat-card">
          <h3>Total Students</h3>
          <p className="stat-value">{students.length}</p>
        </div>
        <div className="stat-card">
          <h3>Active Learners</h3>
          <p className="stat-value">
            {students.filter(s => s.total_quizzes > 0).length}
          </p>
        </div>
        <div className="stat-card">
          <h3>Average Score</h3>
          <p className="stat-value">
            {students.length > 0
              ? (students.reduce((sum, s) => sum + s.average_score, 0) / students.length).toFixed(1)
              : '0.0'}%
          </p>
        </div>
        <div className="stat-card">
          <h3>Students Needing Help</h3>
          <p className="stat-value">
            {students.filter(s => s.average_score < 70 && s.total_quizzes > 0).length}
          </p>
        </div>
      </div>

      {/* Enhanced Charts Section */}
      <div className="charts-section">
        <div className="chart-container">
          <h2>Pathway Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pathwayDistribution}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percentage }) => `${name}: ${percentage}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {pathwayDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[entry.name] || '#8884d8'} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-container">
          <h2>Students per Pathway</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={studentsPerPathway}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="pathway" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" fill="#667eea" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-container">
          <h2>Score Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={scoreDistribution}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="range" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" fill="#17a2b8" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-container">
          <h2>Performance Trend (Top 10 Students)</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={performanceTrend}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="earlier" stroke="#8884d8" name="Earlier Avg" />
              <Line type="monotone" dataKey="recent" stroke="#82ca9d" name="Recent Avg" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-container">
          <h2>Average Scores by Pathway</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={studentsPerPathway.map(pathway => {
              const pathwayStudents = students.filter(s => s.pathway === pathway.pathway);
              const avgScore = pathwayStudents.length > 0
                ? pathwayStudents.reduce((sum, s) => sum + s.average_score, 0) / pathwayStudents.length
                : 0;
              return { pathway: pathway.pathway, avgScore: avgScore.toFixed(1) };
            })}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="pathway" />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Legend />
              <Bar dataKey="avgScore" fill="#28a745" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-container">
          <h2>Quiz Completion Rate</h2>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={students.slice(0, 10).map(s => ({
              name: s.name,
              quizzes: s.total_quizzes,
              score: s.average_score
            }))}>
              <defs>
                <linearGradient id="colorQuizzes" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#667eea" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#667eea" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Area type="monotone" dataKey="quizzes" stroke="#667eea" fillOpacity={1} fill="url(#colorQuizzes)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Students List with Analytics */}
      <div className="students-section">
        <h2>All Students ({students.length})</h2>
        <div className="students-table-container">
          <table className="students-table">
            <thead>
              <tr>
                <th>Select</th>
                <th>Name</th>
                <th>Email</th>
                <th>Pathway</th>
                <th>Average Score</th>
                <th>Quizzes</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredStudents.map((student) => (
                <tr key={student.student_id}>
                  <td>
                    <input 
                      type="checkbox" 
                      checked={selectedStudents.includes(student.student_id)}
                      onChange={() => handleStudentSelect(student.student_id)}
                    />
                  </td>
                  <td>{student.name}</td>
                  <td>{student.email}</td>
                  <td>
                    <PathwayBadge pathway={student.pathway} />
                  </td>
                  <td>
                    <span style={{ color: getPerformanceColor(student.average_score) }}>
                      {student.average_score.toFixed(1)}%
                    </span>
                  </td>
                  <td>{student.total_quizzes}</td>
                  <td>
                    <button 
                      onClick={() => handleStudentClick(student)}
                      className="btn btn-primary btn-sm"
                    >
                      View Analytics
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Pathway Generator Modal */}
      {showPathwayGenerator && (
        <div className="modal-overlay" onClick={() => setShowPathwayGenerator(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Generate Learning Pathway</h2>
              <button className="modal-close-btn" onClick={() => setShowPathwayGenerator(false)}>×</button>
            </div>
            <form onSubmit={handleGeneratePathway} className="modal-body">
              <div className="form-group">
                <label>Select Student:</label>
                <select 
                  value={pathwayForm.studentId} 
                  onChange={(e) => setPathwayForm({...pathwayForm, studentId: e.target.value})}
                  required
                >
                  <option value="">Choose a student...</option>
                  {students.map(s => (
                    <option key={s.student_id} value={s.student_id}>
                      {s.name} ({s.email})
                    </option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label>Pathway Level:</label>
                <select 
                  value={pathwayForm.pathway} 
                  onChange={(e) => setPathwayForm({...pathwayForm, pathway: e.target.value})}
                  required
                >
                  <option value="Basic">Basic</option>
                  <option value="Intermediate">Intermediate</option>
                  <option value="Accelerated">Accelerated</option>
                </select>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={() => setShowPathwayGenerator(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">Generate Pathway</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Task Assignment Modal */}
      {showTaskAssignment && (
        <div className="modal-overlay" onClick={() => setShowTaskAssignment(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Assign Task to Students</h2>
              <button className="modal-close-btn" onClick={() => setShowTaskAssignment(false)}>×</button>
            </div>
            <form onSubmit={handleAssignTask} className="modal-body" onFocus={() => fetchQuizzes()}>
              <div className="form-group">
                <label>Task Title:</label>
                <input 
                  type="text" 
                  value={taskForm.title}
                  onChange={(e) => setTaskForm({...taskForm, title: e.target.value})}
                  required
                  placeholder="Enter task title"
                />
              </div>
              <div className="form-group">
                <label>Description:</label>
                <textarea 
                  value={taskForm.description}
                  onChange={(e) => setTaskForm({...taskForm, description: e.target.value})}
                  required
                  placeholder="Enter task description"
                  rows="4"
                />
              </div>
              <div className="form-group">
                <label>Due Date:</label>
                <input 
                  type="date" 
                  value={taskForm.dueDate}
                  onChange={(e) => setTaskForm({...taskForm, dueDate: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Associated Quiz (Optional):</label>
                <select 
                  value={taskForm.quizId}
                  onChange={(e) => setTaskForm({...taskForm, quizId: e.target.value})}
                >
                  <option value="">No Quiz (Task Only)</option>
                  <option value="default">Auto-select Default Quiz (Based on Student Pathway)</option>
                  {availableQuizzes.map(quiz => (
                    <option key={quiz.quiz_id} value={quiz.quiz_id}>
                      {quiz.title} - {quiz.pathway_id}
                    </option>
                  ))}
                </select>
                <small style={{color: '#666', fontSize: '0.85em', display: 'block', marginTop: '5px'}}>
                  {taskForm.quizId === 'default' 
                    ? 'A default quiz matching the student\'s pathway will be automatically selected.'
                    : 'Select a quiz to associate with this task. Students will be able to take the quiz as part of completing the task.'}
                </small>
              </div>
              <div className="form-group">
                <label>Selected Students: {selectedStudents.length}</label>
                <div className="selected-students-list">
                  {selectedStudents.length === 0 ? (
                    <p className="text-muted">No students selected. Select students from the table above.</p>
                  ) : (
                    <ul>
                      {selectedStudents.map(id => {
                        const student = students.find(s => s.student_id === id);
                        return student ? <li key={id}>{student.name}</li> : null;
                      })}
                    </ul>
                  )}
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={() => setShowTaskAssignment(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">Assign Task</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Student Detail Modal */}
      {showModal && selectedStudent && (
        <StudentDetailModal
          student={selectedStudent}
          onClose={handleCloseModal}
        />
      )}
      </div>
    </div>
  );
}

export default TeacherDashboard;
