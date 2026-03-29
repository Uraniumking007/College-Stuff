// API Configuration
const API_BASE_URL = 'http://localhost:5000/api/todos';

// DOM Elements
const todoForm = document.getElementById('todoForm');
const todoInput = document.getElementById('todoInput');
const todoList = document.getElementById('todoList');
const loading = document.getElementById('loading');
const errorMessage = document.getElementById('errorMessage');
const totalCount = document.getElementById('totalCount');
const completedCount = document.getElementById('completedCount');
const pendingCount = document.getElementById('pendingCount');

// Load todos on page load
document.addEventListener('DOMContentLoaded', loadTodos);

// Form submit handler
todoForm.addEventListener('submit', async (e) => {
   e.preventDefault();
   const text = todoInput.value.trim();

   if (!text) {
      showError('Please enter a todo item');
      return;
   }

   await createTodo(text);
   todoInput.value = '';
   todoInput.focus();
});

// Load all todos
async function loadTodos() {
   showLoading(true);
   hideError();

   try {
      const response = await fetch(API_BASE_URL);
      const result = await response.json();

      if (result.success) {
         renderTodos(result.data);
         updateStats(result.data);
      } else {
         showError('Failed to load todos');
      }
   } catch (error) {
      showError('Error connecting to server. Make sure Docker containers are running.');
      console.error('Error loading todos:', error);
   } finally {
      showLoading(false);
   }
}

// Create new todo
async function createTodo(text) {
   showLoading(true);
   hideError();

   try {
      const response = await fetch(API_BASE_URL, {
         method: 'POST',
         headers: {
            'Content-Type': 'application/json',
         },
         body: JSON.stringify({ text }),
      });

      const result = await response.json();

      if (result.success) {
         await loadTodos();
      } else {
         showError(result.message || 'Failed to create todo');
      }
   } catch (error) {
      showError('Error creating todo');
      console.error('Error creating todo:', error);
   } finally {
      showLoading(false);
   }
}

// Toggle todo completion
async function toggleTodo(id, completed) {
   try {
      const response = await fetch(`${API_BASE_URL}/${id}/toggle`, {
         method: 'PATCH',
      });

      const result = await response.json();

      if (result.success) {
         await loadTodos();
      } else {
         showError('Failed to toggle todo');
      }
   } catch (error) {
      showError('Error toggling todo');
      console.error('Error toggling todo:', error);
   }
}

// Delete todo
async function deleteTodo(id) {
   if (!confirm('Are you sure you want to delete this todo?')) {
      return;
   }

   showLoading(true);

   try {
      const response = await fetch(`${API_BASE_URL}/${id}`, {
         method: 'DELETE',
      });

      const result = await response.json();

      if (result.success) {
         await loadTodos();
      } else {
         showError('Failed to delete todo');
      }
   } catch (error) {
      showError('Error deleting todo');
      console.error('Error deleting todo:', error);
   } finally {
      showLoading(false);
   }
}

// Render todos to DOM
function renderTodos(todos) {
   if (todos.length === 0) {
      todoList.innerHTML = `
            <div class="empty-state">
                <h3>No todos yet! 🎉</h3>
                <p>Add your first todo item above to get started.</p>
            </div>
        `;
      return;
   }

   todoList.innerHTML = todos.map(todo => `
        <div class="todo-item ${todo.completed ? 'completed' : ''}" data-id="${todo._id}">
            <input 
                type="checkbox" 
                class="todo-checkbox" 
                ${todo.completed ? 'checked' : ''}
                onchange="toggleTodo('${todo._id}', ${todo.completed})"
            >
            <div class="todo-text">${escapeHtml(todo.text)}</div>
            <div class="todo-date">${formatDate(todo.createdAt)}</div>
            <div class="todo-actions">
                <button class="btn btn-danger" onclick="deleteTodo('${todo._id}')">
                    Delete
                </button>
            </div>
        </div>
    `).join('');
}

// Update statistics
function updateStats(todos) {
   const total = todos.length;
   const completed = todos.filter(t => t.completed).length;
   const pending = total - completed;

   totalCount.textContent = `Total: ${total}`;
   completedCount.textContent = `Completed: ${completed}`;
   pendingCount.textContent = `Pending: ${pending}`;
}

// Show/hide loading
function showLoading(show) {
   loading.style.display = show ? 'block' : 'none';
}

// Show error message
function showError(message) {
   errorMessage.textContent = message;
   errorMessage.style.display = 'block';
   setTimeout(() => {
      errorMessage.style.display = 'none';
   }, 5000);
}

// Hide error message
function hideError() {
   errorMessage.style.display = 'none';
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
   const div = document.createElement('div');
   div.textContent = text;
   return div.innerHTML;
}

// Format date
function formatDate(dateString) {
   const date = new Date(dateString);
   return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
   });
}

// Make functions available globally for onclick handlers
window.toggleTodo = toggleTodo;
window.deleteTodo = deleteTodo;
