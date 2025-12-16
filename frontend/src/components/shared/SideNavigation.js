/**
 * Side Navigation Component
 * Provides side navigation bar with search and logout functionality
 */
import React, { useState } from 'react';
import Swal from 'sweetalert2';
import './SideNavigation.css';

function SideNavigation({ 
  user, 
  userRole, 
  onLogout, 
  onSearch, 
  searchPlaceholder = "Search...",
  onGeneratePathway,
  onAssignTasks
}) {
  const [isOpen, setIsOpen] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = (e) => {
    const query = e.target.value;
    setSearchQuery(query);
    if (onSearch) {
      onSearch(query);
    }
  };

  const handleLogout = async () => {
    const result = await Swal.fire({
      title: 'Logout?',
      text: 'Are you sure you want to logout?',
      icon: 'question',
      showCancelButton: true,
      confirmButtonColor: '#dc3545',
      cancelButtonColor: '#6c757d',
      confirmButtonText: 'Yes, logout',
      cancelButtonText: 'Cancel'
    });

    if (result.isConfirmed) {
      onLogout();
    }
  };

  const getRoleIcon = () => {
    switch (userRole?.toLowerCase()) {
      case 'student':
        return '👨‍🎓';
      case 'teacher':
        return '👨‍🏫';
      case 'admin':
        return '👨‍💼';
      default:
        return '👤';
    }
  };

  const getRoleName = () => {
    switch (userRole?.toLowerCase()) {
      case 'student':
        return 'Student';
      case 'teacher':
        return 'Teacher';
      case 'admin':
        return 'Admin';
      default:
        return 'User';
    }
  };

  return (
    <div className={`side-nav ${isOpen ? 'open' : 'closed'}`}>
      <div className="side-nav-header">
        <div className="nav-toggle" onClick={() => setIsOpen(!isOpen)}>
          {isOpen ? '←' : '→'}
        </div>
        {isOpen && (
          <>
            <div className="nav-logo">
              <span className="logo-icon">📚</span>
              <span className="logo-text">ILPG</span>
            </div>
          </>
        )}
      </div>

      {isOpen && (
        <>
          <div className="nav-user-info">
            <div className="user-avatar">
              <span className="avatar-icon">{getRoleIcon()}</span>
            </div>
            <div className="user-details">
              <div className="user-name">{user?.name || 'User'}</div>
              <div className="user-role">{getRoleName()}</div>
              <div className="user-email">{user?.email || ''}</div>
            </div>
          </div>

          <div className="nav-search">
            <input
              type="text"
              placeholder={searchPlaceholder}
              value={searchQuery}
              onChange={handleSearch}
              className="search-input"
            />
            <span className="search-icon">🔍</span>
          </div>

          <div className="nav-menu">
            <div className="nav-menu-item active">
              <span className="menu-icon">🏠</span>
              <span className="menu-text">Dashboard</span>
            </div>
            
            {userRole?.toLowerCase() === 'teacher' && (
              <>
                <div 
                  className="nav-menu-item" 
                  onClick={onGeneratePathway}
                  style={{ cursor: 'pointer' }}
                >
                  <span className="menu-icon">🛤️</span>
                  <span className="menu-text">Generate Pathway</span>
                </div>
                <div 
                  className="nav-menu-item" 
                  onClick={onAssignTasks}
                  style={{ cursor: 'pointer' }}
                >
                  <span className="menu-icon">📋</span>
                  <span className="menu-text">Assign Tasks</span>
                </div>
              </>
            )}
          </div>

          <div className="nav-footer">
            <button onClick={handleLogout} className="nav-logout-btn">
              <span className="logout-icon">🚪</span>
              <span className="logout-text">Logout</span>
            </button>
          </div>
        </>
      )}

      {!isOpen && (
        <div className="nav-minimal">
          <div className="nav-user-minimal">
            <span className="avatar-icon-small">{getRoleIcon()}</span>
          </div>
          {userRole?.toLowerCase() === 'teacher' && (
            <>
              <div 
                className="nav-action-minimal" 
                onClick={onGeneratePathway} 
                title="Generate Pathway"
              >
                <span>🛤️</span>
              </div>
              <div 
                className="nav-action-minimal" 
                onClick={onAssignTasks} 
                title="Assign Tasks"
              >
                <span>📋</span>
              </div>
            </>
          )}
          <div className="nav-logout-minimal" onClick={handleLogout} title="Logout">
            <span>🚪</span>
          </div>
        </div>
      )}
    </div>
  );
}

export default SideNavigation;










