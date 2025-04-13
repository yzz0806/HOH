// auth.js
class Auth {
    constructor() {
        this.userRole = sessionStorage.getItem('userRole');
        console.log('Auth initialized, current role:', this.userRole);
    }

    setRole(role) {
        console.log('Setting role to:', role);
        sessionStorage.setItem('userRole', role);
        this.userRole = role;
    }

    getRole() { 
        return this.userRole;
    }

    isAuthenticated() {
        return !!this.userRole;
    }

    logout() {
        sessionStorage.removeItem('userRole');
        window.location.href = '../../index.html';
    }
}

// Initialize auth
const auth = new Auth();

// Make selectRole globally accessible
window.selectRole = function(role) {
    console.log(`selectRole called with role: ${role}`);
    if (role === 'student') {
      window.location.href = 'pages/student/dashboard.html';
    } else if (role === 'teacher') {
      window.location.href = 'pages/teacher/dashboard.html';
    }
  };
  
// Make logout globally accessible
window.logout = function() {
    console.log('Logout called');
    sessionStorage.removeItem('userRole');
    window.location.href = '../../index.html';
};

// Add this to test if the script is loaded
console.log('auth.js loaded');

// Check authentication on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('Page loaded, checking auth...');
    const currentRole = sessionStorage.getItem('userRole');
    console.log('Current role:', currentRole);
    
    if (!currentRole && !window.location.pathname.includes('index.html')) {
        console.log('Not authenticated, redirecting to index');
        window.location.href = '../../index.html';
    }
});

