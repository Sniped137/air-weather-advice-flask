function checkPassword(password) {
    var hasMinLength = password.length >= 8;
    var hasUppercase = /[A-Z]/.test(password);
    var hasNumber = /\d/.test(password);
    var hasSpecial = /[\W_]/.test(password);
    return [hasMinLength, hasUppercase, hasNumber, hasSpecial];
  };

  const emailError = document.getElementById('email-error');
  const emailInput = document.getElementById('email');
  const usernameError = document.getElementById('username-error');
  const usernameInput = document.getElementById('username');
  const passwordError = document.getElementById('password-error');
  const passwordInput= document.getElementById('password');
  const toggleButton = document.querySelector('.toggle-password');
  const alertDiv = document.getElementById('alert-div');
  const checkbox = document.getElementById('checkbox');

  checkbox.addEventListener('change', function(event) {
      if (event.target.checked) {
          alertDiv.classList.add('hidden');
      } else {
          alertDiv.classList.remove('hidden');
      }
  });

  toggleButton.addEventListener("click", function () {
    if (passwordInput.type === "password") {
      passwordInput.type = "text";
    } else {
      passwordInput.type = "password";
    }
  });

  function validateEmail() {
  const email = emailInput.value;
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (emailRegex.test(email)) {
    emailError.classList.add('hidden');
    emailInput.classList.remove('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
    emailInput.classList.add('border-green-500', 'focus:border-green-500', 'focus:ring-green-500');
  } else {
    emailError.classList.remove('hidden');
    emailInput.classList.remove('border-green-500', 'focus:border-green-500', 'focus:ring-green-500');
    emailInput.classList.add('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
  }}

  function validateUsername() {
    const username = usernameInput.value;
    if (username.length > 3 && /^[a-zA-Z0-9]+$/.test(username)) {
      usernameError.classList.add('hidden');
      usernameInput.classList.remove('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
      usernameInput.classList.add('border-green-500', 'focus:border-green-500', 'focus:ring-green-500');
    } else {
      usernameError.classList.remove('hidden');
      usernameInput.classList.remove('border-green-500', 'focus:border-green-500', 'focus:ring-green-500');
      usernameInput.classList.add('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
    }}

    function validatePassword() {
    const password = passwordInput.value;
    if (password.length > 7 && /^(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,}$/.test(password)) {      
      passwordError.classList.add('hidden');
      passwordInput.classList.remove('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
      passwordInput.classList.add('border-green-500', 'focus:border-green-500', 'focus:ring-green-500');
    } else {
      passwordError.classList.remove('hidden');
      passwordInput.classList.remove('border-green-500', 'focus:border-green-500', 'focus:ring-green-500');
      passwordInput.classList.add('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
    }}


  emailInput.addEventListener('input', validateEmail);
  usernameInput.addEventListener('input', validateUsername);
  passwordInput.addEventListener('input', validatePassword);


  document.getElementById("password").addEventListener("input", function() {
  var password = document.getElementById("password").value;
  var result = checkPassword(password);

  document.querySelectorAll(".my-24 li").forEach(function(li, index) {
    var svg = li.querySelector("svg");
    var span = li.querySelector("span");
    if (result[index]) {
      svg.classList.remove("text-red-500");
      svg.classList.add("text-green-500");
      span.classList.remove("text-gray-600");
      span.classList.add("text-green-500");
      svg.innerHTML = '<path d="M15.1965 7.85999C15.1965 3.71785 11.8387 0.359985 7.69653 0.359985C3.5544 0.359985 0.196533 3.71785 0.196533 7.85999C0.196533 12.0021 3.5544 15.36 7.69653 15.36C11.8387 15.36 15.1965 12.0021 15.1965 7.85999Z" fill="currentColor" fill-opacity="0.1"/><path d="M11.5219 4.0949C11.7604 3.81436 12.181 3.78025 12.4617 4.01871C12.7422 4.25717 12.7763 4.6779 12.5378 4.95844L6.87116 11.6251C6.62896 11.91 6.1998 11.94 5.9203 11.6916L2.9203 9.02494C2.64511 8.78033 2.62032 8.35894 2.86493 8.08375C3.10955 7.80856 3.53092 7.78378 3.80611 8.02839L6.29667 10.2423L11.5219 4.0949Z" fill="currentColor"/>';
    } else {
      svg.classList.remove("text-green-500");
      svg.classList.add("text-red-500");
      span.classList.remove("text-green-500");
      span.classList.add("text-gray-600");
      svg.innerHTML = '<path d="M15.1965 7.85999C15.1965 3.71785 11.8387 0.359985 7.69653 0.359985C3.5544 0.359985 0.196533 3.71785 0.196533 7.85999C0.196533 12.0021 3.5544 15.36 7.69653 15.36C11.8387 15.36 15.1965 12.0021 15.1965 7.85999Z" fill="currentColor" fill-opacity="0.1"/><path d="M3 3 L13 13 M3 13 L13 3" stroke="currentColor" stroke-width="1.5" />';
    }})});