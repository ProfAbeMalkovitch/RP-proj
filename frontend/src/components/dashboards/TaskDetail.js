/**
 * Task Detail Component
 * Displays task details and associated quiz
 */
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Swal from 'sweetalert2';
import { tasksAPI, quizAPI, resultsAPI } from '../../services/api';
import TaskQuiz from './TaskQuiz';
import SideNavigation from '../shared/SideNavigation';
import './TaskDetail.css';

function TaskDetail({ student, onLogout, taskId: propTaskId, onTaskComplete }) {
  const { taskId: routeTaskId } = useParams();
  const taskId = propTaskId || routeTaskId; // Use prop if provided, otherwise use route param
  const navigate = useNavigate();
  const [task, setTask] = useState(null);
  const [quiz, setQuiz] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [quizSubmitted, setQuizSubmitted] = useState(false);
  const [existingResult, setExistingResult] = useState(null);
  const [isCompleted, setIsCompleted] = useState(false);

  useEffect(() => {
    fetchTaskData();
  }, [taskId]);

  const fetchTaskData = async () => {
    try {
      setLoading(true);
      setError('');

      // Get student ID - try multiple possible fields
      const studentId = student?.student_id || student?.user_id;
      if (!studentId) {
        setError('Student ID not found');
        setLoading(false);
        return;
      }

      if (!taskId) {
        setError('Task ID not provided');
        setLoading(false);
        return;
      }

      // Get all tasks for the student
      const tasksData = await tasksAPI.getStudentTasks(studentId);
      // Handle both response formats: {tasks: [...], ...} or [...]
      const taskList = tasksData?.tasks || (Array.isArray(tasksData) ? tasksData : []);
      
      // Find the specific task
      const foundTask = taskList.find(t => t.task_id === taskId);
      
      if (!foundTask) {
        setError(`Task not found. Task ID: ${taskId}`);
        setLoading(false);
        return;
      }

      setTask(foundTask);

      // If task has a quiz, fetch it and check if already completed
      if (foundTask.quiz_id) {
        try {
          const quizData = await quizAPI.getQuiz(foundTask.quiz_id);
          setQuiz(quizData);

          // Check if quiz is already completed FOR THIS SPECIFIC TASK
          // Logic: Only prevent quiz if task status is "completed"
          // If task is pending/in-progress, always allow quiz attempt (even if quiz was taken before)
          const userData = JSON.parse(localStorage.getItem('user') || '{}');
          const studentId = userData.user_id || student?.user_id || student?.student_id;
          
          if (foundTask.status === 'completed') {
            // Task is marked as completed - check for quiz result submitted after task was assigned
            try {
              const taskAssignedDate = foundTask.assigned_at;
              
              // Get all quiz results for this student and quiz
              const allResults = await resultsAPI.getStudentResults(studentId);
              const taskAssignedDateTime = new Date(taskAssignedDate);
              
              // Find quiz result for this quiz submitted AFTER task was assigned
              const taskSpecificResult = allResults.find(r => {
                if (r.quiz_id === foundTask.quiz_id) {
                  const resultDate = new Date(r.submitted_at);
                  return resultDate >= taskAssignedDateTime;
                }
                return false;
              });
              
              if (taskSpecificResult) {
                setExistingResult(taskSpecificResult);
                setIsCompleted(true);
                setQuizSubmitted(true);
              } else {
                // Task completed but no quiz result for this task - still prevent
                setIsCompleted(true);
                setQuizSubmitted(true);
              }
            } catch (err) {
              // Error checking results, but task is completed - prevent re-attempt
              setIsCompleted(true);
              setQuizSubmitted(true);
            }
          } else {
            // Task is pending or in-progress - ALWAYS allow quiz attempt
            // Even if student took this quiz before in a different context
            setIsCompleted(false);
            setQuizSubmitted(false);
          }
        } catch (err) {
          console.error('Error fetching quiz:', err);
          setError('Failed to load quiz. Please try again.');
        }
      }
    } catch (err) {
      console.error('Error fetching task:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to load task');
    } finally {
      setLoading(false);
    }
  };

  const handleQuizSubmit = async (answers) => {
    // Prevent submission if already completed
    if (isCompleted || quizSubmitted) {
      Swal.fire({
        icon: 'info',
        title: 'Already Completed',
        text: 'This quiz has already been completed. You cannot submit again.',
        confirmButtonColor: '#667eea',
        confirmButtonText: 'OK'
      });
      return;
    }

    try {
      const userData = JSON.parse(localStorage.getItem('user') || '{}');
      const studentId = userData.user_id || student?.user_id || student?.student_id;

      const submission = {
        student_id: studentId,
        quiz_id: quiz.quiz_id,
        answers: answers
      };

      const result = await resultsAPI.submitQuiz(submission);

      // Update task status to completed if quiz is submitted
      if (task && task.status !== 'completed') {
        try {
          await tasksAPI.updateTaskStatus(task.task_id, 'completed');
          // Refresh task data to get updated status
          await fetchTaskData();
        } catch (err) {
          console.error('Error updating task status:', err);
        }
      }

      // Mark as completed and store result
      setExistingResult(result);
      setIsCompleted(true);
      
      // Show success message and mark quiz as submitted
      setTimeout(async () => {
        setQuizSubmitted(true);
        await Swal.fire({
          icon: 'success',
          title: 'Quiz Submitted!',
          text: `Your score: ${result.percentage?.toFixed(1) || 'N/A'}%`,
          confirmButtonColor: '#667eea',
          confirmButtonText: 'OK'
        });
        
        // Call onTaskComplete callback if provided
        if (onTaskComplete) {
          onTaskComplete();
        }
      }, 500);
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message;
      if (errorMsg.includes('already') || errorMsg.includes('completed')) {
        // Quiz already submitted - fetch result and show it
        try {
          const userData = JSON.parse(localStorage.getItem('user') || '{}');
          const studentId = userData.user_id || student?.user_id || student?.student_id;
          const result = await resultsAPI.getQuizResult(quiz.quiz_id, studentId);
          if (result) {
            setExistingResult(result);
            setIsCompleted(true);
            setQuizSubmitted(true);
            Swal.fire({
              icon: 'info',
              title: 'Already Completed',
              text: 'This quiz has already been completed.',
              confirmButtonColor: '#667eea',
              confirmButtonText: 'OK'
            });
          }
        } catch (fetchErr) {
          Swal.fire({
            icon: 'error',
            title: 'Submission Failed',
            text: `Failed to submit quiz: ${errorMsg}`,
            confirmButtonColor: '#dc3545',
            confirmButtonText: 'OK'
          });
        }
      } else {
        Swal.fire({
          icon: 'error',
          title: 'Submission Failed',
          text: `Failed to submit quiz: ${errorMsg}`,
          confirmButtonColor: '#dc3545',
          confirmButtonText: 'OK'
        });
      }
    }
  };

  const handleBackToDashboard = () => {
    navigate('/dashboard');
  };

  const handleSearch = (query) => {
    // Search functionality can be implemented if needed
  };

  if (loading) {
    return (
      <div className="task-detail-container">
        <SideNavigation 
          user={student} 
          userRole="student" 
          onLogout={onLogout}
          onSearch={handleSearch}
          searchPlaceholder="Search..."
        />
        <div className="dashboard-content">
          <div className="loading">Loading task...</div>
        </div>
      </div>
    );
  }

  if (error && !task) {
    return (
      <div className="task-detail-container">
        <SideNavigation 
          user={student} 
          userRole="student" 
          onLogout={onLogout}
          onSearch={handleSearch}
          searchPlaceholder="Search..."
        />
        <div className="dashboard-content">
          <div className="error-banner">{error}</div>
          <button onClick={handleBackToDashboard} className="btn btn-primary">
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="task-detail-container">
      <SideNavigation 
        user={student} 
        userRole="student" 
        onLogout={onLogout}
        onSearch={handleSearch}
        searchPlaceholder="Search..."
      />
      
      <div className="dashboard-content">
        <header className="task-detail-header">
          <button onClick={handleBackToDashboard} className="btn btn-secondary btn-back">
            ← Back to Dashboard
          </button>
          <h1>Task Details</h1>
        </header>

        {error && <div className="error-banner">{error}</div>}

        {task && (
          <div className="task-detail-content">
            <div className="task-info-card">
              <div className="task-header">
                <h2>{task.title}</h2>
                <span className={`task-status-badge ${task.status}`}>
                  {task.status}
                </span>
              </div>
              
              <div className="task-meta">
                <p><strong>From:</strong> {task.teacher_name || 'Teacher'}</p>
                <p><strong>Due Date:</strong> {new Date(task.due_date).toLocaleDateString()}</p>
                <p><strong>Assigned:</strong> {new Date(task.assigned_at).toLocaleDateString()}</p>
              </div>

              <div className="task-description">
                <h3>Description</h3>
                <p>{task.description}</p>
              </div>

              {task.quiz_info && (
                <div className="task-quiz-info">
                  <h3>Associated Quiz</h3>
                  <p><strong>{task.quiz_info.quiz_title}</strong></p>
                  {task.quiz_info.quiz_description && (
                    <p className="quiz-description">{task.quiz_info.quiz_description}</p>
                  )}
                </div>
              )}
            </div>

            {quiz && (
              <div className="quiz-section">
                {isCompleted && existingResult ? (
                  <div className="quiz-already-completed">
                    <div className="completed-header">
                      <div className="completed-icon">✅</div>
                      <h2>Quiz Already Completed</h2>
                    </div>
                    <div className="quiz-result-card">
                      <div className="result-score">
                        <div className="score-circle">
                          <span className="score-percentage">{existingResult.percentage?.toFixed(1) || '0'}%</span>
                        </div>
                        <div className="score-details">
                          <p className="score-text">Score: {existingResult.score || 0} / {existingResult.total_points || 0} points</p>
                          <p className="submitted-date">
                            Completed on: {new Date(existingResult.submitted_at).toLocaleString()}
                          </p>
                        </div>
                      </div>
                      <div className="result-message">
                        <p>This quiz has already been completed. You cannot retake it.</p>
                      </div>
                    </div>
                    <div className="completed-actions">
                      <button onClick={handleBackToDashboard} className="btn btn-primary">
                        Back to Dashboard
                      </button>
                    </div>
                  </div>
                ) : quizSubmitted ? (
                  <div className="quiz-completed">
                    <p>✅ Task quiz completed! You can return to the dashboard.</p>
                    <button onClick={handleBackToDashboard} className="btn btn-primary">
                      Back to Dashboard
                    </button>
                  </div>
                ) : (
                  <div className="task-quiz-wrapper">
                    <TaskQuiz 
                      quiz={quiz} 
                      onSubmit={handleQuizSubmit}
                      taskTitle={task.title}
                    />
                  </div>
                )}
              </div>
            )}

            {!quiz && task.quiz_id && (
              <div className="quiz-loading">
                <p>Loading quiz...</p>
              </div>
            )}

            {!task.quiz_id && (
              <div className="no-quiz-message">
                <p>This task does not have an associated quiz.</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default TaskDetail;


