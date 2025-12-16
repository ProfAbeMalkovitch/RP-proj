/**
 * Quiz Component
 * Displays quiz questions and handles submission
 */
import React, { useState } from 'react';
import Swal from 'sweetalert2';
import './Quiz.css';

function Quiz({ quiz, onSubmit }) {
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);

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
      text: 'Are you sure you want to submit this quiz?',
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

  if (submitted) {
    return (
      <div className="quiz-submitted">
        <h3>Quiz Submitted Successfully!</h3>
        <p>Your answers have been submitted. Check your results on the dashboard.</p>
      </div>
    );
  }

  return (
    <div className="quiz-container">
      <div className="quiz-header">
        <h2>{quiz.title}</h2>
        <p className="quiz-description">{quiz.description}</p>
        <div className="quiz-info">
          <span>{quiz.questions.length} Questions</span>
          <span>{quiz.total_points} Total Points</span>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="quiz-form">
        {quiz.questions.map((question, index) => (
          <div key={question.question_id} className="question-card">
            <div className="question-header">
              <h3>
                Question {index + 1} of {quiz.questions.length}
              </h3>
              <span className="question-points">{question.points || 10} points</span>
            </div>
            <p className="question-text">{question.question_text}</p>
            <div className="options-list">
              {question.options.map((option, optionIndex) => (
                <label
                  key={optionIndex}
                  className={`option-label ${
                    answers[question.question_id] === optionIndex ? 'selected' : ''
                  }`}
                >
                  <input
                    type="radio"
                    name={question.question_id}
                    value={optionIndex}
                    checked={answers[question.question_id] === optionIndex}
                    onChange={() => handleAnswerChange(question.question_id, optionIndex)}
                    required
                  />
                  <span className="option-text">{option}</span>
                </label>
              ))}
            </div>
          </div>
        ))}

        <div className="quiz-footer">
          <div className="progress-info">
            Answered: {Object.keys(answers).length} / {quiz.questions.length}
          </div>
          <button type="submit" className="btn btn-primary submit-btn">
            Submit Quiz
          </button>
        </div>
      </form>
    </div>
  );
}

export default Quiz;









