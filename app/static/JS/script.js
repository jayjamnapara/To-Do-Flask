// Client-side form validations (simple, non-WTF)
function _showError(msg) {
	// Use alert for simplicity; server-side flashes will also appear.
	alert(msg);
}

function validateEmail(email) {
	return /^\S+@\S+\.\S+$/.test(email);
}

function validateRegisterForm() {
	const fullname = document.getElementById('fullname')?.value || '';
	const email = document.getElementById('email')?.value || '';
	const phone = document.getElementById('phone')?.value || '';
	const password = document.getElementById('password')?.value || '';

	if (!fullname.trim() || !email.trim() || !phone.trim() || !password) {
		_showError('Please fill all required fields.');
		return false;
	}

	if (!validateEmail(email)) {
		_showError('Enter a valid email address.');
		return false;
	}

	if (!/^\d{7,15}$/.test(phone)) {
		_showError('Phone must be digits only (7-15 digits).');
		return false;
	}

	if (password.length < 6) {
		_showError('Password must be at least 6 characters.');
		return false;
	}

	return true;
}

function validateLoginForm() {
	const email = document.getElementById('login-email')?.value || '';
	const password = document.getElementById('login-password')?.value || '';

	if (!email.trim() || !password) {
		_showError('Email and password are required.');
		return false;
	}
	if (!validateEmail(email)) {
		_showError('Enter a valid email address.');
		return false;
	}
	return true;
}

function validateTaskForm(form) {
	// form can be passed from onsubmit
	const titleEl = form ? form.querySelector('input[name="title"]') : document.getElementById('task-title');
	const dueEl = form ? form.querySelector('input[name="due_date"]') : document.getElementById('task-due');
	const title = titleEl ? titleEl.value : '';
	const due = dueEl ? dueEl.value : '';

	if (!title || !title.trim()) {
		_showError('Task title is required.');
		return false;
	}

	if (!due) {
		_showError('Due date is required.');
		return false;
	}

	// Basic YYYY-MM-DD check
	if (!/^\d{4}-\d{2}-\d{2}$/.test(due)) {
		_showError('Due date format invalid. Use YYYY-MM-DD.');
		return false;
	}

	return true;
}

// Expose functions for inline onsubmit calls (already global in browsers)

