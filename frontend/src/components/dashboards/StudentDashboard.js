/**
 * Student Dashboard Component
 * Shows student's pathway, quizzes, mind map, roadmap, and study guide
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Swal from 'sweetalert2';
import { analyticsAPI, pathwayAPI, quizAPI, roadmapAPI, tasksAPI, adaptiveAPI, resultsAPI } from '../../services/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import MindMap from '../MindMap';
import Roadmap from '../Roadmap';
import Quiz from '../Quiz';
import PathwayBadge from '../shared/PathwayBadge';
import SideNavigation from '../shared/SideNavigation';
import GenerateRoadmapButton from '../GenerateRoadmapButton';
import ConceptMasteryCard from '../shared/ConceptMasteryCard';
import RecommendationsCard from '../shared/RecommendationsCard';
import TaskDetail from './TaskDetail';
import './StudentDashboard.css';

function StudentDashboard({ student, onLogout }) {
  const navigate = useNavigate();
  const [studentData, setStudentData] = useState(null);
  const [pathway, setPathway] = useState(null);
  const [generatedRoadmap, setGeneratedRoadmap] = useState(null);
  const [quizzes, setQuizzes] = useState([]);
  const [quizHistory, setQuizHistory] = useState([]);
  const [assignedTasks, setAssignedTasks] = useState([]);
  const [masteryData, setMasteryData] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [selectedTask, setSelectedTask] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [selectedQuiz, setSelectedQuiz] = useState(null);
  const [deletedTaskIds, setDeletedTaskIds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchStudentData();
  }, []);

  const fetchStudentData = async () => {
    try {
      setLoading(true);
      
      // Get student quiz history and dashboard data
      // Use student_id if available, otherwise use user_id
      const studentId = student.student_id || student.user_id;
      const history = await analyticsAPI.getStudentQuizHistory(studentId);
      setQuizHistory(history.quiz_history || []);
      setStudentData(history);

      // Get pathway based on student's pathway
      const pathwayName = history.pathway.toLowerCase();
      const pathwayId = `pathway_${pathwayName}`;
      
      try {
        const pathwayData = await pathwayAPI.getPathway(pathwayId);
        setPathway(pathwayData);
        
        // Get quizzes for this pathway
        if (pathwayData.quiz_ids && pathwayData.quiz_ids.length > 0) {
          const quizzesData = await Promise.allSettled(
            pathwayData.quiz_ids.map((quizId) => quizAPI.getQuiz(quizId))
          );
          const successfulQuizzes = quizzesData
            .filter((result) => result.status === 'fulfilled')
            .map((result) => result.value);
          setQuizzes(successfulQuizzes);
        }
      } catch (err) {
        console.warn('Pathway not found, using default');
      }

      // Try to fetch active generated roadmap
      try {
        const activeRoadmap = await roadmapAPI.getActiveRoadmap(studentId);
        if (activeRoadmap && activeRoadmap.roadmap) {
          setGeneratedRoadmap(activeRoadmap.roadmap);
        }
      } catch (err) {
        // No active roadmap, that's okay
        console.log('No active generated roadmap');
      }

      // Fetch teacher-assigned tasks
      try {
        const tasks = await tasksAPI.getStudentTasks(studentId);
        setAssignedTasks(tasks.tasks || tasks || []);
      } catch (err) {
        console.error('Error fetching tasks:', err);
        setAssignedTasks([]);
      }

      // Fetch concept mastery data
      try {
        const mastery = await adaptiveAPI.getMastery(studentId);
        setMasteryData(mastery);
      } catch (err) {
        console.error('Error fetching mastery data:', err);
        setMasteryData(null);
      }

      // Fetch recommendations
      try {
        const recs = await adaptiveAPI.getRecommendations(studentId);
        setRecommendations(recs.recommendations || recs || []);
      } catch (err) {
        console.error('Error fetching recommendations:', err);
        setRecommendations([]);
      }

    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to load student data';
      setError(errorMessage);
      console.error('Error fetching student data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleQuizSelect = (quiz) => {
    setSelectedQuiz(quiz);
    setSelectedTask(null); // Clear any selected task
    // Ensure we're on the quizzes tab
    if (activeTab !== 'quizzes') {
      setActiveTab('quizzes');
    }
  };

  const handleQuizSubmit = async (answers) => {
    try {
      const studentId = student.student_id || student.user_id;
      const submission = {
        student_id: studentId,
        quiz_id: selectedQuiz.quiz_id,
        answers: answers
      };
      
      const result = await resultsAPI.submitQuiz(submission);
      
      // Show success message
      await Swal.fire({
        icon: 'success',
        title: 'Quiz Submitted!',
        text: `Your score: ${result.percentage.toFixed(1)}%`,
        confirmButtonColor: '#667eea',
        confirmButtonText: 'OK'
      });
      
      // Clear selected quiz and refresh data
      setSelectedQuiz(null);
      await fetchStudentData();
    } catch (err) {
      console.error('Error submitting quiz:', err);
      Swal.fire({
        icon: 'error',
        title: 'Submission Failed',
        text: 'Failed to submit quiz. Please try again.',
        confirmButtonColor: '#dc3545',
        confirmButtonText: 'OK'
      });
    }
  };

  const handleDeleteTask = async (taskId, e) => {
    e.stopPropagation();
    const result = await Swal.fire({
      title: 'Remove Task?',
      text: 'Are you sure you want to remove this task from your dashboard? (This will not delete it from the database)',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#dc3545',
      cancelButtonColor: '#6c757d',
      confirmButtonText: 'Yes, remove it',
      cancelButtonText: 'Cancel'
    });

    if (result.isConfirmed) {
      setDeletedTaskIds([...deletedTaskIds, taskId]);
      Swal.fire({
        icon: 'success',
        title: 'Removed!',
        text: 'Task has been removed from your dashboard.',
        confirmButtonColor: '#667eea',
        confirmButtonText: 'OK',
        timer: 2000,
        showConfirmButton: true
      });
    }
  };

  const isDueDatePassed = (dueDate) => {
    if (!dueDate) return false;
    const due = new Date(dueDate);
    const now = new Date();
    return now > due;
  };

  if (loading) {
    return (
      <div className="student-dashboard-container">
        <SideNavigation 
          user={student} 
          userRole="student" 
          onLogout={onLogout}
          searchPlaceholder="Search..."
        />
        <div className="dashboard-content">
          <div className="loading">Loading your dashboard...</div>
        </div>
      </div>
    );
  }

  if (error || !studentData) {
    return (
      <div className="student-dashboard-container">
        <SideNavigation 
          user={student} 
          userRole="student" 
          onLogout={onLogout}
          searchPlaceholder="Search..."
        />
        <div className="dashboard-content">
          <div className="error-banner">{error || 'Failed to load data'}</div>
        </div>
      </div>
    );
  }

  return (
    <div className="student-dashboard-container">
      <SideNavigation 
        user={student} 
        userRole="student" 
        onLogout={onLogout}
        searchPlaceholder="Search..."
      />
      
      <div className="dashboard-content">
        {/* Header with Pathway Badge */}
        <header className="student-dashboard-header">
          <div className="header-content">
            <div>
              <h1>Welcome, {student.name}</h1>
              <PathwayBadge pathway={studentData.pathway} />
            </div>
            <div className="header-actions">
              <span className="student-email">{student.email}</span>
            </div>
          </div>
        </header>

      {/* Stats Cards */}
      <div className="stats-section">
        <div className="stat-card">
          <h3>Average Score</h3>
          <p className="stat-value">{studentData.average_score.toFixed(1)}%</p>
        </div>
        <div className="stat-card">
          <h3>Quizzes Completed</h3>
          <p className="stat-value">{studentData.total_quizzes}</p>
        </div>
        <div className="stat-card">
          <h3>Current Pathway</h3>
          <p className="stat-value">{studentData.pathway}</p>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="tabs">
        <button
          className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button
          className={`tab ${activeTab === 'quizzes' ? 'active' : ''}`}
          onClick={() => setActiveTab('quizzes')}
        >
          Quizzes
        </button>
        {pathway && (
          <>
            <button
              className={`tab ${activeTab === 'mindmap' ? 'active' : ''}`}
              onClick={() => setActiveTab('mindmap')}
            >
              Mind Map
            </button>
            <button
              className={`tab ${activeTab === 'roadmap' ? 'active' : ''}`}
              onClick={() => setActiveTab('roadmap')}
            >
              Roadmap
            </button>
            <button
              className={`tab ${activeTab === 'studyguide' ? 'active' : ''}`}
              onClick={() => setActiveTab('studyguide')}
            >
              Study Guide
            </button>
          </>
        )}
      </div>

      {/* Tab Content */}
      <div className="tab-content">
        {activeTab === 'overview' && (
          <div className="overview-section">
            <h2>Your Progress</h2>
            
            {/* Concept Mastery Card */}
            {masteryData && (
              <div style={{ marginBottom: 'var(--spacing-lg)' }}>
                <ConceptMasteryCard masteryData={masteryData} />
              </div>
            )}

            {/* Recommendations Card */}
            {recommendations.length > 0 && (
              <div style={{ marginBottom: 'var(--spacing-lg)' }}>
                <RecommendationsCard 
                  recommendations={recommendations}
                  studentId={student.student_id || student.user_id}
                />
              </div>
            )}

            {/* Quiz History Chart */}
            <div className="quiz-history-chart">
              <h3>Quiz History</h3>
              {quizHistory.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={quizHistory}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="quizNumber" />
                    <YAxis domain={[0, 100]} />
                    <Tooltip />
                    <Legend />
                    <Line
                      type="monotone"
                      dataKey="score"
                      stroke="#667eea"
                      strokeWidth={2}
                      name="Score (%)"
                    />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <p>No quiz history yet. Complete quizzes to see your progress!</p>
              )}
            </div>

            {/* Teacher-Assigned Tasks */}
            {assignedTasks.filter(t => !deletedTaskIds.includes(t.task_id)).length > 0 && (
              <div className="assigned-tasks-section" style={{ marginTop: 'var(--spacing-lg)' }}>
                <h2>📋 Tasks Assigned by Teacher</h2>
                <div className="tasks-grid">
                  {assignedTasks
                    .filter(t => !deletedTaskIds.includes(t.task_id))
                    .map((task) => {
                      const dueDatePassed = isDueDatePassed(task.due_date);
                      const canTakeQuiz = task.quiz_id && !dueDatePassed && task.status !== 'completed';
                      
                      return (
                        <div 
                          key={task.task_id} 
                          className={`task-card ${task.status} ${canTakeQuiz ? 'clickable' : ''}`}
                          onClick={() => canTakeQuiz && setSelectedTask(task)}
                          style={{ cursor: canTakeQuiz ? 'pointer' : 'default', opacity: dueDatePassed ? 0.7 : 1 }}
                        >
                          <div className="task-header">
                            <h4>{task.title}</h4>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                              <span className={`task-status-badge ${task.status}`}>
                                {task.status}
                              </span>
                              <button
                                onClick={(e) => handleDeleteTask(task.task_id, e)}
                                className="task-delete-btn"
                                title="Remove from dashboard"
                              >
                                ✕
                              </button>
                            </div>
                          </div>
                          <p className="task-description">{task.description}</p>
                          {task.teacher_name && (
                            <p className="task-teacher">Assigned by: {task.teacher_name}</p>
                          )}
                          {task.due_date && (
                            <p className={`task-footer ${dueDatePassed ? 'due-date-closed' : ''}`}>
                              Due: {new Date(task.due_date).toLocaleDateString()}
                              {dueDatePassed && (
                                <span className="closed-badge">⚠️ Due Date Closed</span>
                              )}
                            </p>
                          )}
                          {task.quiz_id && task.quiz_info && (
                            <div className="task-quiz-info">
                              <strong>📝 Quiz Available:</strong> {task.quiz_info.quiz_title}
                              {dueDatePassed && (
                                <p className="closed-message" style={{ color: '#dc3545', marginTop: '8px', fontWeight: 'bold' }}>
                                  ⚠️ Due date is closed. This quiz is no longer available.
                                </p>
                              )}
                            </div>
                          )}
                        </div>
                      );
                    })}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'quizzes' && (
          <div className="quizzes-section">
            <h2>Available Quizzes</h2>
            
            {/* Show selected task quiz */}
            {selectedTask ? (
              <div>
                <button
                  onClick={() => setSelectedTask(null)}
                  className="btn btn-secondary"
                  style={{ marginBottom: '20px' }}
                >
                  ← Back to Quiz List
                </button>
                <TaskDetail 
                  student={student} 
                  taskId={selectedTask.task_id}
                  onTaskComplete={() => {
                    setSelectedTask(null);
                    fetchStudentData(); // Refresh data
                  }}
                  onLogout={onLogout}
                />
              </div>
            ) : selectedQuiz ? (
              <div>
                <button
                  onClick={() => setSelectedQuiz(null)}
                  className="btn btn-secondary"
                  style={{ marginBottom: '20px' }}
                >
                  ← Back to Quiz List
                </button>
                <Quiz quiz={selectedQuiz} onSubmit={handleQuizSubmit} />
              </div>
            ) : (
              <div>
                {/* Teacher-Assigned Task Quizzes */}
                {assignedTasks.filter(t => t.quiz_id && t.status !== 'completed' && !isDueDatePassed(t.due_date)).length > 0 && (
                  <div style={{ marginBottom: 'var(--spacing-lg)' }}>
                    <h3>📋 Quizzes from Assigned Tasks</h3>
                    <div className="quiz-list">
                      {assignedTasks
                        .filter(t => t.quiz_id && t.status !== 'completed' && !isDueDatePassed(t.due_date))
                        .map((task) => (
                          <div key={task.task_id} className="quiz-card">
                            <h3>{task.quiz_info?.quiz_title || 'Task Quiz'}</h3>
                            <p>{task.quiz_info?.quiz_description || task.description}</p>
                            <p className="quiz-info">
                              Task: {task.title} • Assigned by: {task.teacher_name}
                            </p>
                            <button
                              onClick={() => setSelectedTask(task)}
                              className="btn btn-primary"
                            >
                              Start Task Quiz
                            </button>
                          </div>
                        ))}
                    </div>
                  </div>
                )}

                {/* Pathway Quizzes */}
                <h3>📚 Pathway Quizzes</h3>
                <div className="quiz-list">
                  {quizzes.length > 0 ? (
                    quizzes.map((quiz) => (
                      <div key={quiz.quiz_id} className="quiz-card">
                        <h3>{quiz.title}</h3>
                        <p>{quiz.description}</p>
                        <p className="quiz-info">
                          {quiz.questions?.length || 0} Questions • {quiz.total_points} Points
                        </p>
                        <button
                          onClick={() => handleQuizSelect(quiz)}
                          className="btn btn-primary"
                        >
                          Start Quiz
                        </button>
                      </div>
                    ))
                  ) : (
                    <p>No quizzes available for your pathway.</p>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'mindmap' && pathway && (
          <div className="mindmap-section">
            <h2>Topic Mind Map</h2>
            <MindMap 
              topics={pathway.topics} 
              studentId={student.student_id || student.user_id}
            />
          </div>
        )}

        {activeTab === 'roadmap' && (
          <div className="roadmap-section">
            <h2>Learning Roadmap</h2>
            
            {/* Generate Roadmap Button */}
            <div style={{ marginBottom: '20px' }}>
              <GenerateRoadmapButton 
                studentId={student.student_id || student.user_id}
                onRoadmapGenerated={(roadmap) => {
                  setGeneratedRoadmap(roadmap);
                  // Refresh pathway data if needed
                  if (pathway) {
                    fetchStudentData();
                  }
                }}
              />
            </div>

            {/* Display Generated Roadmap or Pathway Roadmap */}
            {generatedRoadmap ? (
              <Roadmap 
                roadmap={generatedRoadmap.tasks || generatedRoadmap.roadmap || generatedRoadmap}
                studentId={student.student_id || student.user_id}
              />
            ) : pathway && pathway.roadmap ? (
              <Roadmap 
                roadmap={pathway.roadmap} 
                studentId={student.student_id || student.user_id}
              />
            ) : (
              <div style={{ padding: '20px', textAlign: 'center', color: 'var(--text-secondary)' }}>
                <p>No roadmap available. Generate a personalized roadmap using the button above.</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'studyguide' && pathway && (
          <div className="study-guide-section">
            <h2>Study Guide</h2>
            <div className="study-guide-content">
              <div className="guide-section">
                <h3>Pathway Overview</h3>
                <p>{pathway.description}</p>
              </div>
              <div className="guide-section">
                <h3>Learning Content</h3>
                <div className="content-text">{pathway.content}</div>
              </div>
              <div className="guide-section">
                <h3>Key Topics</h3>
                <ul>
                  {pathway.topics?.map((topic, idx) => (
                    <li key={idx}>{topic.name}</li>
                  ))}
                </ul>
              </div>
              <div className="guide-section">
                <h3>Guidance Activities</h3>
                <div className="activities-list">
                  {pathway.roadmap?.map((task, idx) => (
                    <div key={idx} className="activity-item">
                      <h4>{task.title}</h4>
                      <p>Order: {task.order}</p>
                      <span className={`status-badge ${task.status}`}>{task.status}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
      </div>
    </div>
  );
}

export default StudentDashboard;

