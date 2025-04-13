class Dashboard {
    constructor() {
        this.userRole = auth.getRole();
        this.initializeDashboard();
    }

    async initializeDashboard() {
        this.loadClasses();
        this.setupEventListeners();
    }

    // Sample class data (replace with actual API calls)
    async loadClasses() {
        const classes = [
            {
                id: 1,
                name: 'Mathematics 101',
                time: '9:00 AM',
                status: 'upcoming',
                description: 'Introduction to Calculus'
            },
            {
                id: 2,
                name: 'Physics 101',
                time: '11:00 AM',
                status: 'completed',
                description: 'Basic Mechanics'
            }
        ];

        this.displayClasses(classes);
        this.displayUpcomingClasses(classes.filter(c => c.status === 'upcoming'));
    }

    displayClasses(classes) {
        const gallery = document.querySelector('.class-gallery');
        if (!gallery) return;

        gallery.innerHTML = classes.map(cls => this.createClassCard(cls)).join('');
    }

    createClassCard(cls) {
        return `
            <div class="col-md-6 col-lg-4 mb-4">
                <div class="class-card">
                    <h3>${cls.name}</h3>
                    <span class="status ${cls.status}">${cls.status}</span>
                    <p>${cls.description}</p>
                    <p>Time: ${cls.time}</p>
                    <button class="btn btn-primary" onclick="enterClass(${cls.id})">
                        ${cls.status === 'upcoming' ? 'Enter Class' : 'View Recording'}
                    </button>
                </div>
            </div>
        `;
    }

    displayUpcomingClasses(classes) {
        const upcomingList = document.querySelector('.upcoming-classes .card-body');
        if (!upcomingList) return;

        upcomingList.innerHTML = classes.map(cls => `
            <div class="class-time">
                <div class="time-indicator">${cls.time}</div>
                <div class="class-info">
                    <strong>${cls.name}</strong>
                    <div>${cls.description}</div>
                </div>
            </div>
        `).join('');
    }

    setupEventListeners() {
        if (this.userRole === 'teacher') {
            const createClassBtn = document.querySelector('#createClassBtn');
            if (createClassBtn) {
                createClassBtn.addEventListener('click', () => this.showCreateClassModal());
            }
        }
    }

    showCreateClassModal() {
        // Implementation for creating a new class
        const modal = new bootstrap.Modal(document.getElementById('createClassModal'));
        modal.show();
    }
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    const dashboard = new Dashboard();
});

// Navigation function
function enterClass(classId) {
    const userRole = auth.getRole();
    window.location.href = `../pages/${userRole}/classroom.html?id=${classId}`;
}