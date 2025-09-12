// 🌟 Tab Organizer Pro - ADHD Friendly JavaScript 🧠✨

// 📊 Global state management
let documents = JSON.parse(localStorage.getItem('tabOrganizerDocuments') || '[]');
let currentStep = 1;
let currentDocumentId = null;

// 🎯 Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Tab Organizer Pro initialized!');
    loadDocuments();
    updateProgressIndicator();
    
    // Add some encouraging messages for ADHD users
    showWelcomeMessage();
});

// 🎉 Welcome message for ADHD-friendly onboarding
function showWelcomeMessage() {
    const messages = [
        "🎯 You've got this! Let's organize those tabs! 💪",
        "🌟 Ready to turn chaos into clarity? ✨",
        "🧠 Time to give your brain some peace! 🕯️",
        "📋 Let's make organization fun and easy! 🎨"
    ];
    
    const randomMessage = messages[Math.floor(Math.random() * messages.length)];
    console.log(randomMessage);
    
    // Show a brief success message
    setTimeout(() => {
        showNotification(randomMessage, 'success');
    }, 500);
}

// 📝 Input form management
function showTabInput() {
    hideAllInputForms();
    document.getElementById('tab-input').classList.remove('hidden');
    updateProgressIndicator(1);
    showNotification('🌐 Ready to capture that tab! Paste the URL and content below.', 'info');
}

function showTextInput() {
    hideAllInputForms();
    document.getElementById('text-input').classList.remove('hidden');
    updateProgressIndicator(1);
    showNotification('✍️ Time to add your content! Give it a good title.', 'info');
}

function showFileInput() {
    hideAllInputForms();
    document.getElementById('file-input').classList.remove('hidden');
    updateProgressIndicator(1);
    showNotification('📁 Drag and drop your file, or click to browse!', 'info');
}

function hideAllInputForms() {
    const forms = document.querySelectorAll('.input-form');
    forms.forEach(form => form.classList.add('hidden'));
}

// 💾 Content saving functions
function saveTabContent() {
    const url = document.getElementById('tab-url').value.trim();
    const title = document.getElementById('tab-title').value.trim();
    const content = document.getElementById('tab-content').value.trim();
    
    if (!title && !content) {
        showNotification('🚨 Please add at least a title or some content!', 'error');
        return;
    }
    
    const doc = {
        id: generateId(),
        title: title || 'Untitled Tab',
        content: content,
        url: url,
        type: 'tab',
        createdAt: new Date().toISOString(),
        size: content.length
    };
    
    addDocument(doc);
    clearTabForm();
    updateProgressIndicator(2);
    showNotification('🎉 Tab content saved! Great job! ✨', 'success');
}

function saveTextContent() {
    const title = document.getElementById('content-title').value.trim();
    const content = document.getElementById('content-text').value.trim();
    
    if (!title && !content) {
        showNotification('🚨 Please add at least a title or some content!', 'error');
        return;
    }
    
    const doc = {
        id: generateId(),
        title: title || 'Untitled Document',
        content: content,
        type: 'text',
        createdAt: new Date().toISOString(),
        size: content.length
    };
    
    addDocument(doc);
    clearTextForm();
    updateProgressIndicator(2);
    showNotification('🎉 Content saved successfully! You\'re doing great! 🌟', 'success');
}

// 📁 File handling
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const doc = {
                id: generateId(),
                title: file.name,
                content: e.target.result,
                type: 'file',
                createdAt: new Date().toISOString(),
                size: e.target.result.length,
                fileName: file.name
            };
            
            addDocument(doc);
            updateProgressIndicator(2);
            showNotification(`📁 File "${file.name}" loaded successfully! 🎯`, 'success');
        };
        reader.readAsText(file);
    }
}

// 🎯 Drag and drop handling
function dragOverHandler(event) {
    event.preventDefault();
    event.currentTarget.style.backgroundColor = '#e3f2fd';
}

function dropHandler(event) {
    event.preventDefault();
    event.currentTarget.style.backgroundColor = '';
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];
        const reader = new FileReader();
        reader.onload = function(e) {
            const doc = {
                id: generateId(),
                title: file.name,
                content: e.target.result,
                type: 'file',
                createdAt: new Date().toISOString(),
                size: e.target.result.length,
                fileName: file.name
            };
            
            addDocument(doc);
            updateProgressIndicator(2);
            showNotification(`🎯 Dropped file "${file.name}" successfully! Amazing! ✨`, 'success');
        };
        reader.readAsText(file);
    }
}

// 📚 Document management
function addDocument(document) {
    documents.push(document);
    saveDocuments();
    loadDocuments();
}

function loadDocuments() {
    const container = document.getElementById('documents-container');
    
    if (documents.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <h3>🎯 Ready to organize!</h3>
                <p>Add your first piece of content above to get started! 🚀</p>
                <p>💡 <strong>Pro tip:</strong> Start with just one tab to build momentum! 💪</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = documents.map(doc => `
        <div class="document-card" onclick="openDocument('${doc.id}')">
            <div class="document-title">
                ${getDocumentIcon(doc.type)} ${escapeHtml(doc.title)}
            </div>
            <div class="document-meta">
                📅 ${formatDate(doc.createdAt)} • 📏 ${formatSize(doc.size)}
                ${doc.url ? `• 🔗 <span style="color: #2196F3;">${escapeHtml(doc.url.substring(0, 30))}...</span>` : ''}
            </div>
            <div class="document-preview">
                ${escapeHtml(doc.content.substring(0, 150))}${doc.content.length > 150 ? '...' : ''}
            </div>
        </div>
    `).join('');
}

function getDocumentIcon(type) {
    const icons = {
        'tab': '🌐',
        'text': '📝',
        'file': '📁',
        'default': '📄'
    };
    return icons[type] || icons.default;
}

function openDocument(id) {
    const doc = documents.find(d => d.id === id);
    if (!doc) return;
    
    currentDocumentId = id;
    const modal = document.getElementById('document-modal');
    const title = document.getElementById('modal-title');
    const body = document.getElementById('modal-body');
    
    title.textContent = `${getDocumentIcon(doc.type)} ${doc.title}`;
    
    // Create a nice preview of the content
    body.innerHTML = `
        <div style="margin-bottom: 20px;">
            <div style="display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 15px;">
                <span><strong>📅 Created:</strong> ${formatDate(doc.createdAt)}</span>
                <span><strong>📏 Size:</strong> ${formatSize(doc.size)}</span>
                <span><strong>🏷️ Type:</strong> ${doc.type.toUpperCase()}</span>
            </div>
            ${doc.url ? `<div style="margin-bottom: 15px;"><strong>🔗 URL:</strong> <a href="${escapeHtml(doc.url)}" target="_blank" style="color: #2196F3;">${escapeHtml(doc.url)}</a></div>` : ''}
        </div>
        <div style="background: #f5f5f5; padding: 20px; border-radius: 8px; border-left: 4px solid #4CAF50; max-height: 400px; overflow-y: auto;">
            <pre style="white-space: pre-wrap; font-family: inherit; margin: 0;">${escapeHtml(doc.content)}</pre>
        </div>
    `;
    
    modal.classList.remove('hidden');
    updateProgressIndicator(3);
}

function closeModal() {
    document.getElementById('document-modal').classList.add('hidden');
    currentDocumentId = null;
    updateProgressIndicator(2);
}

// 📤 Export functions
function exportDocument() {
    if (!currentDocumentId) return;
    
    const doc = documents.find(d => d.id === currentDocumentId);
    if (!doc) return;
    
    const blob = new Blob([doc.content], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${doc.title}.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showNotification(`📤 "${doc.title}" exported successfully! 🎉`, 'success');
    closeModal();
}

function exportAllDocuments() {
    if (documents.length === 0) {
        showNotification('📭 No documents to export yet! Add some content first.', 'warning');
        return;
    }
    
    // Create a combined HTML file with all documents
    const combinedHtml = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📚 My Organized Documents - Tab Organizer Pro</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 20px; 
            line-height: 1.6; 
        }
        .document { 
            margin-bottom: 40px; 
            padding: 20px; 
            border-left: 5px solid #4CAF50; 
            background: #f9f9f9; 
            border-radius: 8px; 
        }
        .document-title { 
            font-size: 1.5em; 
            color: #4CAF50; 
            margin-bottom: 10px; 
        }
        .document-meta { 
            color: #666; 
            margin-bottom: 20px; 
            font-size: 0.9em; 
        }
        .document-content { 
            background: white; 
            padding: 15px; 
            border-radius: 5px; 
            border: 1px solid #ddd; 
        }
        .toc { 
            background: #e8f5e8; 
            padding: 20px; 
            border-radius: 8px; 
            margin-bottom: 30px; 
        }
        .toc h2 { 
            color: #4CAF50; 
            margin-top: 0; 
        }
        .toc a { 
            color: #2196F3; 
            text-decoration: none; 
        }
        .toc a:hover { 
            text-decoration: underline; 
        }
    </style>
</head>
<body>
    <h1>📚 My Organized Documents</h1>
    <p>🌟 Generated by Tab Organizer Pro on ${new Date().toLocaleDateString()}</p>
    
    <div class="toc">
        <h2>📋 Table of Contents</h2>
        ${documents.map(doc => `<div>• <a href="#doc-${doc.id}">${getDocumentIcon(doc.type)} ${escapeHtml(doc.title)}</a></div>`).join('')}
    </div>
    
    ${documents.map(doc => `
        <div class="document" id="doc-${doc.id}">
            <div class="document-title">${getDocumentIcon(doc.type)} ${escapeHtml(doc.title)}</div>
            <div class="document-meta">
                📅 Created: ${formatDate(doc.createdAt)} | 📏 Size: ${formatSize(doc.size)} | 🏷️ Type: ${doc.type.toUpperCase()}
                ${doc.url ? `| 🔗 <a href="${escapeHtml(doc.url)}" target="_blank">Original URL</a>` : ''}
            </div>
            <div class="document-content">
                <pre style="white-space: pre-wrap; font-family: inherit; margin: 0;">${escapeHtml(doc.content)}</pre>
            </div>
        </div>
    `).join('')}
    
    <footer style="margin-top: 50px; text-align: center; color: #666; font-size: 0.9em;">
        <p>🌟 Created with Tab Organizer Pro - Making organization ADHD-friendly! 🧠✨</p>
    </footer>
</body>
</html>`;
    
    const blob = new Blob([combinedHtml], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `all-documents-${new Date().toISOString().split('T')[0]}.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showNotification(`📤 All ${documents.length} documents exported! Great work! 🎉`, 'success');
    updateProgressIndicator(3);
}

// ✏️ Edit and delete functions
function editDocument() {
    if (!currentDocumentId) return;
    
    const doc = documents.find(d => d.id === currentDocumentId);
    if (!doc) return;
    
    const newTitle = prompt(`✏️ Edit title for "${doc.title}":`, doc.title);
    const newContent = prompt(`📝 Edit content:`, doc.content);
    
    if (newTitle !== null && newTitle.trim()) {
        doc.title = newTitle.trim();
    }
    if (newContent !== null) {
        doc.content = newContent;
        doc.size = newContent.length;
    }
    
    saveDocuments();
    loadDocuments();
    closeModal();
    showNotification('✏️ Document updated successfully! 🎯', 'success');
}

function deleteDocument() {
    if (!currentDocumentId) return;
    
    const doc = documents.find(d => d.id === currentDocumentId);
    if (!doc) return;
    
    if (confirm(`🗑️ Are you sure you want to delete "${doc.title}"?`)) {
        documents = documents.filter(d => d.id !== currentDocumentId);
        saveDocuments();
        loadDocuments();
        closeModal();
        showNotification(`🗑️ "${doc.title}" deleted successfully.`, 'info');
    }
}

// 📋 Document management functions
function createNewDocument() {
    const title = prompt('📝 Enter title for new document:', 'New Document');
    if (!title) return;
    
    const content = prompt('📄 Enter content for new document:', '');
    
    const doc = {
        id: generateId(),
        title: title.trim(),
        content: content || '',
        type: 'manual',
        createdAt: new Date().toISOString(),
        size: (content || '').length
    };
    
    addDocument(doc);
    showNotification(`📝 "${title}" created successfully! 🌟`, 'success');
}

function sortDocuments() {
    const sortBy = document.getElementById('sort-options').value;
    
    switch (sortBy) {
        case 'date':
            documents.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
            break;
        case 'title':
            documents.sort((a, b) => a.title.localeCompare(b.title));
            break;
        case 'size':
            documents.sort((a, b) => b.size - a.size);
            break;
    }
    
    saveDocuments();
    loadDocuments();
    showNotification(`📊 Documents sorted by ${sortBy}! 🎯`, 'info');
}

// 🔧 Utility functions
function generateId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function formatSize(bytes) {
    if (bytes < 1024) return bytes + ' chars';
    if (bytes < 1024 * 1024) return Math.round(bytes / 1024) + ' KB';
    return Math.round(bytes / (1024 * 1024)) + ' MB';
}

function saveDocuments() {
    localStorage.setItem('tabOrganizerDocuments', JSON.stringify(documents));
}

function clearTabForm() {
    document.getElementById('tab-url').value = '';
    document.getElementById('tab-title').value = '';
    document.getElementById('tab-content').value = '';
    hideAllInputForms();
}

function clearTextForm() {
    document.getElementById('content-title').value = '';
    document.getElementById('content-text').value = '';
    hideAllInputForms();
}

// 📊 Progress indicator
function updateProgressIndicator(step = currentStep) {
    currentStep = step;
    const steps = document.querySelectorAll('.step');
    
    steps.forEach((stepEl, index) => {
        if (index + 1 <= step) {
            stepEl.classList.add('active');
        } else {
            stepEl.classList.remove('active');
        }
    });
}

// 🔔 Notification system
function showNotification(message, type = 'info') {
    // Remove any existing notifications
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        z-index: 9999;
        max-width: 400px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
    
    // Set background color based on type
    const colors = {
        'success': '#4CAF50',
        'error': '#f44336',
        'warning': '#FF9800',
        'info': '#2196F3'
    };
    
    notification.style.backgroundColor = colors[type] || colors.info;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto remove after 4 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        }
    }, 4000);
}

// 🎹 Keyboard shortcuts for power users
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + N for new document
    if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
        e.preventDefault();
        createNewDocument();
    }
    
    // Ctrl/Cmd + E for export all
    if ((e.ctrlKey || e.metaKey) && e.key === 'e') {
        e.preventDefault();
        exportAllDocuments();
    }
    
    // Escape to close modal
    if (e.key === 'Escape') {
        closeModal();
    }
});

// 🔄 Auto-save reminder
setInterval(() => {
    if (documents.length > 0) {
        console.log('💾 Auto-saving your progress...');
        saveDocuments();
    }
}, 30000); // Save every 30 seconds

// 🌟 Motivational messages for ADHD users
const motivationalMessages = [
    "🎯 You're doing great! Every document organized is a win! 🏆",
    "🧠 Your future self will thank you for this organization! 💝",
    "🌟 Look at you being productive! Keep it up! 💪",
    "📚 Your digital space is getting cleaner by the minute! ✨",
    "🎉 Organization superstar in action! 🌟"
];

// Show motivational message every few documents
function checkForMotivationalMessage() {
    if (documents.length > 0 && documents.length % 3 === 0) {
        const message = motivationalMessages[Math.floor(Math.random() * motivationalMessages.length)];
        setTimeout(() => showNotification(message, 'success'), 1000);
    }
}

// Call this when documents are added
const originalAddDocument = addDocument;
addDocument = function(document) {
    originalAddDocument(document);
    checkForMotivationalMessage();
};