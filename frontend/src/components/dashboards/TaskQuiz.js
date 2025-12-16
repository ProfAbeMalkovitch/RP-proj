/**
 * Task Quiz Component (Special Quiz)
 * Special quiz component designed for task assignments
 * Has different styling and behavior from regular quizzes
 */
import React, { useState } from 'react';
import Swal from 'sweetalert2';
import './TaskQuiz.css';

function TaskQuiz({ quiz, onSubmit, taskTitle }) {
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [currentQuestion, setCurrentQuestion] = useState(0);

  if (!quiz || !quiz.questions) {
    return <p>No quiz data available.</p>;
  }

  // Handle answer selection
  const handleAnswerChange = (questionId, optionIndex) => {
    setAnswers({
      ...answers,
      [questionId]: optionIndex,
    });
  };

  // Handle next question
  const handleNext = () => {
    if (currentQuestion < quiz.questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  // Handle previous question
  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Check if all questions are answered
    const allAnswered = quiz.questions.every(
      (question) => answers[question.question_id] !== undefined
    );

    if (!allAnswered) {
      Swal.fire({
        icon: 'warning',
        title: 'Incomplete Quiz',
        text: 'Please answer all questions before submitting.',
        confirmButtonColor: '#667eea',
        confirmButtonText: 'OK'
      });
      return;
    }

    const result = await Swal.fire({
      title: 'Submit Quiz?',
      text: 'Are you sure you want to submit this quiz? Once submitted, you cannot change your answers.',
      icon: 'question',
      showCancelButton: true,
      confirmButtonColor: '#667eea',
      cancelButtonColor: '#6c757d',
      confirmButtonText: 'Yes, submit it',
      cancelButtonText: 'Cancel'
    });

    if (result.isConfirmed) {
      onSubmit(answers);
      setSubmitted(true);
    }
  };

  // Calculate progress
  const progress = ((Object.keys(answers).length / quiz.questions.length) * 100).toFixed(0);
  const answeredCount = Object.keys(answers).length;
  const currentQuestionData = quiz.questions[currentQuestion];
  const isAnswered = answers[currentQuestionData.question_id] !== undefined;

  if (submitted) {
    return (
      <div className="task-quiz-submitted">
        <div className="submission-icon">✅</div>
        <h3>Quiz Submitted Successfully!</h3>
        <p>Your answers have been submitted for this task.</p>
        <p className="submission-note">You will receive your results shortly.</p>
      </div>
    );
  }

  return (
    <div className="task-quiz-container">
      <div className="task-quiz-header">
        <div className="task-quiz-title-section">
          <h2>{quiz.title || 'Task Quiz'}</h2>
          {quiz.description && (
            <p className="quiz-description">{quiz.description}</p>
          )}
          <div className="task-quiz-info">
            <span className="info-badge">{quiz.questions.length} Questions</span>
            <span className="info-badge">{quiz.total_points} Total Points</span>
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="task-quiz-progress">
        <div className="progress-bar">
          <div 
            className="progress-fill" 
            style={{ width: `${progress}%` }}
          ></div>
        </div>
        <div className="progress-text">
          Answered: {answeredCount} / {quiz.questions.length}
        </div>
      </div>

      {/* Question Navigation */}
      <div className="question-navigation">
        {quiz.questions.map((question, index) => (
          <button
            key={question.question_id}
            className={`question-nav-btn ${
              index === currentQuestion ? 'active' : ''
            } ${
              answers[question.question_id] !== undefined ? 'answered' : ''
            }`}
            onClick={() => setCurrentQuestion(index)}
            title={question.question_text.substring(0, 50) + '...'}
          >
            {index + 1}
          </button>
        ))}
      </div>

      {/* Current Question */}
      <form onSubmit={handleSubmit} className="task-quiz-form">
        <div className="task-question-card">
          <div className="question-number-header">
            <span className="question-number">
              Question {currentQuestion + 1} of {quiz.questions.length}
            </span>
            <span className="question-points">{currentQuestionData.points || 10} points</span>
          </div>
          
          <div className="question-content">
            <h3 className="question-text">{currentQuestionData.question_text}</h3>
            
            <div className="task-options-list">
              {currentQuestionData.options.map((option, optionIndex) => (
                <label
                  key={optionIndex}
                  className={`task-option-label ${
                    answers[currentQuestionData.question_id] === optionIndex ? 'selected' : ''
                  }`}
                >
                  <input
                    type="radio"
                    name={currentQuestionData.question_id}
                    value={optionIndex}
                    checked={answers[currentQuestionData.question_id] === optionIndex}
                    onChange={() => handleAnswerChange(currentQuestionData.question_id, optionIndex)}
                    required={currentQuestion === quiz.questions.length - 1}
                  />
                  <span className="option-letter">
                    {String.fromCharCode(65 + optionIndex)}.
                  </span>
                  <span className="option-text">{option}</span>
                </label>
              ))}
            </div>
          </div>
        </div>

        {/* Navigation Buttons */}
        <div className="task-quiz-navigation">
          <button
            type="button"
            onClick={handlePrevious}
            disabled={currentQuestion === 0}
            className="btn btn-secondary nav-btn"
          >
            ← Previous
          </button>
          
          <div className="navigation-center">
            {currentQuestion + 1} / {quiz.questions.length}
          </div>

          {currentQuestion < quiz.questions.length - 1 ? (
            <button
              type="button"
              onClick={handleNext}
              disabled={!isAnswered}
              className="btn btn-primary nav-btn"
            >
              Next →
            </button>
          ) : (
            <button
              type="submit"
              disabled={!isAnswered || answeredCount < quiz.questions.length}
              className="btn btn-primary btn-submit-task-quiz"
            >
              Submit Quiz
            </button>
          )}
        </div>

        {/* Quick Submit (if all answered) */}
        {answeredCount === quiz.questions.length && (
          <div className="quick-submit-section">
            <p className="all-answered-notice">✓ All questions answered!</p>
            <button
              type="submit"
              className="btn btn-primary btn-submit-all"
            >
              Submit All Answers
            </button>
          </div>
        )}
      </form>
    </div>
  );
}

export default TaskQuiz;









