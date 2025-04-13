class Classroom {
    constructor() {
        this.userRole = auth.getRole();
        this.classId = new URLSearchParams(window.location.search).get('id');
        this.initializeClassroom();
    }

    async initializeClassroom() {
        this.setupWebRTC();
        this.setupChat();
        this.setupSubtitles();
        if (this.userRole === 'teacher') {
            this.setupTeacherControls();
        }
    }

    setupWebRTC() {
        // WebRTC implementation would go here
        // This is a placeholder for the actual WebRTC implementation
        console.log('Setting up WebRTC...');
    }

    setupChat() {
        const chatInput = document.querySelector('.chat-input input');
        const sendButton = document.querySelector('.chat-input button');

        if (chatInput && sendButton) {
            sendButton.addEventListener('click', () => {
                const message = chatInput.value.trim();
                if (message) {
                    this.sendChatMessage(message);
                    chatInput.value = '';
                }
            });

            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    sendButton.click();
                }
            });
        }
    }

    sendChatMessage(message) {
        const chatMessages = document.querySelector('.chat-messages');
        const messageElement = document.createElement('div');
        messageElement.className = 'message sent';
        messageElement.textContent = message;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Here you would typically send the message to your backend
    }

    setupSubtitles() {
        if ('webkitSpeechRecognition' in window) {
            const recognition = new webkitSpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = true;

            recognition.onresult = (event) => {
                const subtitles = document.getElementById('subtitles');
                let interimTranscript = '';
                
                for (let i = event.resultIndex; i < event.results.length; ++i) {
                    if (event.results[i].isFinal) {
                        subtitles.textContent = event.results[i][0].transcript;
                    } else {
                        interimTranscript += event.results[i][0].transcript;
                        subtitles.textContent = interimTranscript;
                    }
                }
            };

            if (this.userRole === 'teacher') {
                recognition.start();
            }
        }
    }

    setupTeacherControls() {
        const toggleStream = document.getElementById('toggleStream');
        const shareScreen = document.getElementById('shareScreen');
        const uploadMaterial = document.getElementById('uploadMaterial');
        const createQuiz = document.getElementById('createQuiz');

        if (toggleStream) {
            toggleStream.addEventListener('click', () => this.toggleVideoStream());
        }

        if (shareScreen) {
            shareScreen.addEventListener('click', () => this.shareScreen());
        }

        if (uploadMaterial) {
            uploadMaterial.addEventListener('click', () => this.showUploadMaterialDialog());
        }

        if (createQuiz) {
            createQuiz.addEventListener('click', () => this.showCreateQuizModal());
        }
    }

    toggleVideoStream() {
        // Implementation for toggling video stream
        console.log('Toggling video stream...');
    }

    shareScreen() {
        if (navigator.mediaDevices.getDisplayMedia) {
            navigator.mediaDevices.getDisplayMedia({ video: true })
                .then(stream => {
                    // Handle screen sharing stream
                    console.log('Screen sharing started');
                })
                .catch(err => {
                    console.error('Error sharing screen:', err);
                });
        }
    }

    showUploadMaterialDialog() {
        // Implementation for material upload
        console.log('Showing upload material dialog...');
    }

    showCreateQuizModal() {
        const modal = new bootstrap.Modal(document.getElementById('quizModal'));
        modal.show();
    }
}

// Initialize classroom
document.addEventListener('DOMContentLoaded', () => {
    const classroom = new Classroom();
});

// Caption WebSocket handling
function initializeCaptions() {
    // Use the correct IP address where your server is running
    const captionSocket = new WebSocket('ws://localhost:8765');
    const subtitlesDiv = document.getElementById('subtitles');

    captionSocket.onopen = function(event) {
        console.log('WebSocket connection established');
        subtitlesDiv.textContent = 'Caption service connected...';
    };

    captionSocket.onmessage = function(event) {
        try {
            const data = JSON.parse(event.data);
            if (data.type === 'caption') {
                console.log('Received caption:', data.text);
                subtitlesDiv.textContent = data.text;
                storeCaptionHistory(data);
            }
        } catch (error) {
            console.error('Error processing caption:', error);
        }
    };

    captionSocket.onclose = function(event) {
        console.log('Caption WebSocket connection closed');
        subtitlesDiv.textContent = 'Caption service disconnected...';
        // Attempt to reconnect after 5 seconds
        setTimeout(initializeCaptions, 5000);
    };

    captionSocket.onerror = function(error) {
        console.error('Caption WebSocket error:', error);
        subtitlesDiv.textContent = 'Caption service error...';
    };
}

// Store caption history
let captionHistory = [];
function storeCaptionHistory(caption) {
    captionHistory.push(caption);
    // Keep only last 100 captions
    if (captionHistory.length > 100) {
        captionHistory.shift();
    }
}

// Function to download caption history
function downloadCaptions() {
    const captionsText = captionHistory
        .map(c => `[${new Date(c.timestamp * 1000).toISOString()}] ${c.text}`)
        .join('\n');
    const blob = new Blob([captionsText], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'captions.txt';
    a.click();
    window.URL.revokeObjectURL(url);
}

// Initialize when the document is loaded
document.addEventListener('DOMContentLoaded', initializeCaptions);