/**
 * Admin Dashboard Component
 * Shows pathways, teachers, students, and categorized pathways
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { studentAPI, teacherAPI, pathwayAPI } from '../services/api';
import { 
  PieChart, Pie, Cell, BarChart, Bar, 
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer 
} from 'recharts';
import PathwayBadge from './shared/PathwayBadge';
import SideNavigation from './shared/SideNavigation';
import './AdminDashboard.css';

const COLORS = {
  Basic: '#FFC107',
  Intermediate: '#17A2B8',
  Accelerated: '#28A745'
};

function AdminDashboard({ admin, onLogout }) {
  const [students, setStudents] = useState([]);
  const [teachers, setTeachers] = useState([]);
  const [pathways, setPathways] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('overview');
  const [searchQuery, setSearchQuery] = useState('');
  const [filteredData, setFilteredData] = useState({ students: [], teachers: [], pathways: [] });
  const navigate = useNavigate();

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError('');
      
      // Fetch all data in parallel
      const [studentsData, teachersData, pathwaysData] = await Promise.all([
        studentAPI.getAllStudents(),
        teacherAPI.getAllTeachers(),
        pathwayAPI.getAllPathways()
      ]);
      
      const studentsList = studentsData || [];
      const teachersList = teachersData || [];
      const pathwaysList = pathwaysData || [];
      
      setStudents(studentsList);
      setTeachers(teachersList);
      setPathways(pathwaysList);
      setFilteredData({ students: studentsList, teachers: teachersList, pathways: pathwaysList });
    } catch (err) {
      setError('Failed to load dashboard data. Please try again.');
      console.error('Error fetching dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  // Categorize students by pathway
  const categorizeStudentsByPathway = () => {
    const categorized = {
      Basic: [],
      Intermediate: [],
      Accelerated: []
    };
    
    students.forEach(student => {
      const pathway = student.pathway || 'Basic';
      if (categorized[pathway]) {
        categorized[pathway].push(student);
      }
    });
    
    return categorized;
  };

  const handleSearch = (query) => {
    setSearchQuery(query);
    if (query.trim() === '') {
      setFilteredData({ students, teachers, pathways });
    } else {
      const filteredStudents = students.filter(item => 
        item.name?.toLowerCase().includes(query.toLowerCase()) ||
        item.email?.toLowerCase().includes(query.toLowerCase()) ||
        item.pathway?.toLowerCase().includes(query.toLowerCase())
      );
      const filteredTeachers = teachers.filter(item => 
        item.name?.toLowerCase().includes(query.toLowerCase()) ||
        item.email?.toLowerCase().includes(query.toLowerCase())
      );
      const filteredPathways = pathways.filter(item => 
        item.name?.toLowerCase().includes(query.toLowerCase()) ||
        item.description?.toLowerCase().includes(query.toLowerCase()) ||
        item.level?.toLowerCase().includes(query.toLowerCase())
      );
      setFilteredData({ students: filteredStudents, teachers: filteredTeachers, pathways: filteredPathways });
    }
  };

  useEffect(() => {
    if (searchQuery.trim() === '') {
      setFilteredData({ students, teachers, pathways });
    }
  }, [students, teachers, pathways, searchQuery]);

  const categorizedStudents = categorizeStudentsByPathway();

  // Generate pathway distribution data
  const pathwayDistribution = [
    { name: 'Basic', value: categorizedStudents.Basic.length },
    { name: 'Intermediate', value: categorizedStudents.Intermediate.length },
    { name: 'Accelerated', value: categorizedStudents.Accelerated.length }
  ];

  if (loading) {
    return (
      <div className="admin-dashboard-container">
        <div className="loading">Loading dashboard...</div>
      </div>
    );
  }

  return (
    <div className="admin-dashboard-container">
      <SideNavigation 
        user={admin} 
        userRole="admin" 
        onLogout={onLogout}
        onSearch={handleSearch}
        searchPlaceholder="Search students, teachers, pathways..."
      />
      
      <div className="dashboard-content">
        <header className="admin-dashboard-header">
          <div className="header-content">
            <h1>Admin Dashboard</h1>
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
          <h3>Total Teachers</h3>
          <p className="stat-value">{teachers.length}</p>
        </div>
        <div className="stat-card">
          <h3>Total Pathways</h3>
          <p className="stat-value">{pathways.length}</p>
        </div>
        <div className="stat-card">
          <h3>Active Pathways</h3>
          <p className="stat-value">
            {pathways.filter(p => p.roadmap && p.roadmap.length > 0).length}
          </p>
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
          className={`tab ${activeTab === 'pathways' ? 'active' : ''}`}
          onClick={() => setActiveTab('pathways')}
        >
          Pathways
        </button>
        <button
          className={`tab ${activeTab === 'teachers' ? 'active' : ''}`}
          onClick={() => setActiveTab('teachers')}
        >
          Teachers
        </button>
        <button
          className={`tab ${activeTab === 'students' ? 'active' : ''}`}
          onClick={() => setActiveTab('students')}
        >
          Students
        </button>
      </div>

      {/* Tab Content */}
      <div className="tab-content">
        {activeTab === 'overview' && (
          <div className="overview-section">
            <h2>System Overview</h2>
            
            {/* Pathway Distribution Chart */}
            <div className="chart-container">
              <h3>Student Distribution by Pathway</h3>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={pathwayDistribution}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, value }) => `${name}: ${value}`}
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

            {/* Quick Stats */}
            <div className="quick-stats-grid">
              <div className="quick-stat-card">
                <h4>Students by Pathway</h4>
                <ul>
                  <li>Basic: {categorizedStudents.Basic.length} students</li>
                  <li>Intermediate: {categorizedStudents.Intermediate.length} students</li>
                  <li>Accelerated: {categorizedStudents.Accelerated.length} students</li>
                </ul>
              </div>
              <div className="quick-stat-card">
                <h4>System Health</h4>
                <ul>
                  <li>Active Students: {students.filter(s => s.quiz_scores && s.quiz_scores.length > 0).length}</li>
                  <li>Average Score: {
                    students.length > 0
                      ? (students.reduce((sum, s) => sum + (s.average_score || 0), 0) / students.length).toFixed(1)
                      : '0.0'
                  }%</li>
                  <li>Total Quizzes Completed: {
                    students.reduce((sum, s) => sum + (s.quiz_scores?.length || 0), 0)
                  }</li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'pathways' && (
          <div className="pathways-section">
            <h2>Learning Pathways ({pathways.length})</h2>
            <div className="pathways-grid">
              {filteredData.pathways.map((pathway) => (
                <div key={pathway.pathway_id} className="pathway-card">
                  <div className="pathway-header">
                    <h3>{pathway.name}</h3>
                    <PathwayBadge pathway={pathway.level} />
                  </div>
                  <p className="pathway-description">{pathway.description}</p>
                  <div className="pathway-stats">
                    <span>{pathway.roadmap?.length || 0} Tasks</span>
                    <span>{pathway.quiz_ids?.length || 0} Quizzes</span>
                    <span>{pathway.topics?.length || 0} Topics</span>
                  </div>
                  <div className="pathway-students">
                    <strong>Students in this pathway: </strong>
                    {categorizedStudents[pathway.level]?.length || 0}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'teachers' && (
          <div className="teachers-section">
            <h2>Teachers ({teachers.length})</h2>
            <div className="teachers-table-container">
              <table className="teachers-table">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Teacher ID</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredData.teachers.map((teacher) => (
                    <tr key={teacher.teacher_id}>
                      <td>{teacher.name}</td>
                      <td>{teacher.email}</td>
                      <td>{teacher.teacher_id}</td>
                      <td>
                        <span className="status-badge active">Active</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'students' && (
          <div className="students-section">
            <h2>Students by Pathway</h2>
            
            {/* Basic Pathway Students */}
            <div className="pathway-category">
              <h3>
                <PathwayBadge pathway="Basic" /> Basic Pathway ({categorizedStudents.Basic.length} students)
              </h3>
              <div className="students-table-container">
                <table className="students-table">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Email</th>
                      <th>Student ID</th>
                      <th>Average Score</th>
                      <th>Quizzes</th>
                    </tr>
                  </thead>
                  <tbody>
                    {categorizedStudents.Basic.map((student) => (
                      <tr key={student.student_id}>
                        <td>{student.name}</td>
                        <td>{student.email}</td>
                        <td>{student.student_id}</td>
                        <td>{(student.average_score || 0).toFixed(1)}%</td>
                        <td>{student.quiz_scores?.length || 0}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Intermediate Pathway Students */}
            <div className="pathway-category">
              <h3>
                <PathwayBadge pathway="Intermediate" /> Intermediate Pathway ({categorizedStudents.Intermediate.length} students)
              </h3>
              <div className="students-table-container">
                <table className="students-table">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Email</th>
                      <th>Student ID</th>
                      <th>Average Score</th>
                      <th>Quizzes</th>
                    </tr>
                  </thead>
                  <tbody>
                    {categorizedStudents.Intermediate.map((student) => (
                      <tr key={student.student_id}>
                        <td>{student.name}</td>
                        <td>{student.email}</td>
                        <td>{student.student_id}</td>
                        <td>{(student.average_score || 0).toFixed(1)}%</td>
                        <td>{student.quiz_scores?.length || 0}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Accelerated Pathway Students */}
            <div className="pathway-category">
              <h3>
                <PathwayBadge pathway="Accelerated" /> Accelerated Pathway ({categorizedStudents.Accelerated.length} students)
              </h3>
              <div className="students-table-container">
                <table className="students-table">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Email</th>
                      <th>Student ID</th>
                      <th>Average Score</th>
                      <th>Quizzes</th>
                    </tr>
                  </thead>
                  <tbody>
                    {categorizedStudents.Accelerated.map((student) => (
                      <tr key={student.student_id}>
                        <td>{student.name}</td>
                        <td>{student.email}</td>
                        <td>{student.student_id}</td>
                        <td>{(student.average_score || 0).toFixed(1)}%</td>
                        <td>{student.quiz_scores?.length || 0}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </div>
      </div>
    </div>
  );
}

export default AdminDashboard;
