/**
 * Pathway Detail Component
 * Displays pathway content, mind map, roadmap, and quizzes
 */
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { pathwayAPI, quizAPI, resultsAPI } from '../services/api';
import MindMap from './MindMap';
import Roadmap from './Roadmap';
import Quiz from './Quiz';
import QuizResultModal from './QuizResultModal';
import './PathwayDetail.css';

function PathwayDetail({ student }) {
  const { pathwayId } = useParams();
  const navigate = useNavigate();
  const [pathway, setPathway] = useState(null);
  const [quizzes, setQuizzes] = useState([]);
  const [activeTab, setActiveTab] = useState('content');
  const [selectedQuiz, setSelectedQuiz] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [quizResult, setQuizResult] = useState(null);
  const [showResultModal, setShowResultModal] = useState(false);

  // Fetch pathway and quizzes on component mount
  useEffect(() => {
    fetchPathwayData();
  }, [pathwayId]);

  // Fetch pathway and associated quizzes
  const fetchPathwayData = async () => {
    try {
      setLoading(true);
      setError('');
      const pathwayData = await pathwayAPI.getPathway(pathwayId);
      setPathway(pathwayData);

      // Fetch quizzes for this pathway
      if (pathwayData.quiz_ids && pathwayData.quiz_ids.length > 0) {
        try {
          const quizzesData = await Promise.allSettled(
          pathwayData.quiz_ids.map((quizId) => quizAPI.getQuiz(quizId))
        );
          // Filter out failed requests and extract successful results
          const successfulQuizzes = quizzesData
            .filter((result) => result.status === 'fulfilled')
            .map((result) => result.value);
          setQuizzes(successfulQuizzes);
          
          // Log any failed quiz fetches but don't block the pathway from loading
          const failedQuizzes = quizzesData.filter((result) => result.status === 'rejected');
          if (failedQuizzes.length > 0) {
            console.warn('Some quizzes failed to load:', failedQuizzes);
          }
        } catch (quizErr) {
          console.error('Error fetching quizzes:', quizErr);
          // Don't set error state - pathway can still be viewed without quizzes
        }
      }
    } catch (err) {
      setError('Failed to load pathway data. Please try again.');
      console.error('Error fetching pathway:', err);
      if (err.response) {
        console.error('Response status:', err.response.status);
        console.error('Response data:', err.response.data);
      }
    } finally {
      setLoading(false);
    }
  };

  // Handle quiz selection
  const handleQuizSelect = (quiz) => {
    setSelectedQuiz(quiz);
    setActiveTab('quizzes');
  };

  // Handle quiz submission
  const handleQuizSubmit = async (answers) => {
    try {
      const submission = {
        student_id: student.student_id,
        quiz_id: selectedQuiz.quiz_id,
        answers: answers,
      };
      const result = await resultsAPI.submitQuiz(submission);
      setQuizResult(result);
      setShowResultModal(true);
      // Reset selected quiz after submission
      setSelectedQuiz(null);
      setActiveTab('quizzes');
    } catch (err) {
      alert('Failed to submit quiz. Please try again.');
      console.error('Error submitting quiz:', err);
    }
  };

  // Handle result modal close
  const handleCloseResultModal = () => {
    setShowResultModal(false);
    setQuizResult(null);
    // Refresh student data to update cumulative score
    window.location.reload();
  };

  if (loading) {
    return (
      <div className="pathway-detail-container">
        <div className="loading">Loading pathway...</div>
      </div>
    );
  }

  if (error || !pathway) {
    return (
      <div className="pathway-detail-container">
        <div className="error-banner">{error || 'Pathway not found'}</div>
        <button onClick={() => navigate('/dashboard')} className="btn btn-primary">
          Back to Dashboard
        </button>
      </div>
    );
  }

  return (
    <div className="pathway-detail-container">
      <header className="pathway-header">
        <button onClick={() => navigate('/dashboard')} className="btn btn-secondary">
          ← Back to Dashboard
        </button>
        <h1>{pathway.name}</h1>
        <span className="pathway-level-badge">{pathway.level}</span>
      </header>

      <div className="pathway-content">
        {/* Tab Navigation */}
        <div className="tabs">
          <button
            className={`tab ${activeTab === 'content' ? 'active' : ''}`}
            onClick={() => setActiveTab('content')}
          >
            Content
          </button>
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
            className={`tab ${activeTab === 'quizzes' ? 'active' : ''}`}
            onClick={() => setActiveTab('quizzes')}
          >
            Quizzes ({quizzes.length})
          </button>
        </div>

        {/* Tab Content */}
        <div className="tab-content">
          {activeTab === 'content' && (
            <div className="content-section">
              <h2>Pathway Content</h2>
              <div className="content-text">{pathway.content}</div>
            </div>
          )}

          {activeTab === 'mindmap' && (
            <div className="mindmap-section">
              <h2>Topic Mind Map</h2>
              <MindMap topics={pathway.topics} studentId={student?.user_id || student?.student_id} />
            </div>
          )}

          {activeTab === 'roadmap' && (
            <div className="roadmap-section">
              <h2>Learning Roadmap</h2>
              <Roadmap roadmap={pathway.roadmap} />
            </div>
          )}

          {activeTab === 'quizzes' && (
            <div className="quizzes-section">
              <h2>Interactive Quizzes</h2>
              {selectedQuiz ? (
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
                    <p>No quizzes available for this pathway.</p>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Quiz Result Modal */}
      {showResultModal && quizResult && (
        <QuizResultModal
          result={quizResult}
          onClose={handleCloseResultModal}
        />
      )}
    </div>
  );
}

export default PathwayDetail;




