function validatePassword() {
    const password = document.getElementById('password').value;
    const length = document.getElementById('length');
    const uppercase = document.getElementById('uppercase');
    const special = document.getElementById('special');

    length.classList.toggle('text-success', password.length >= 8);
    uppercase.classList.toggle('text-success', /[A-Z]/.test(password));
    special.classList.toggle('text-success', /[!@#$%^&*(),.?":{}|<>]/.test(password));
}

// Attach event listener to the password field
document.getElementById('password').addEventListener('input', validatePassword);
