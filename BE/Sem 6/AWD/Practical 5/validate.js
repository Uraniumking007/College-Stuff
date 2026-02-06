function validateForm() {
  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirmPassword").value;
  const phone = document.getElementById("phone").value;
  const age = document.getElementById("age").value;
  const genderElements = document.getElementsByName("gender");

  const nameError = document.getElementById("nameError");
  const emailError = document.getElementById("emailError");
  const passwordError = document.getElementById("passwordError");
  const confirmPasswordError = document.getElementById("confirmPasswordError");
  const phoneError = document.getElementById("phoneError");
  const ageError = document.getElementById("ageError");
  const genderError = document.getElementById("genderError");

  let gender = "";
  for (const element of genderElements) {
    if (element.checked) {
      gender = element.value;
      break;
    }
  }

  let errors = [];
  const passwordRegex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$/;
  const phoneRegex = /^\d{10}$/;

  if (name.trim() === "") {
    errors.push("Name is required. Max 15 characters.");
  }
  if (email.trim() === "" || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    errors.push("Valid email is required.");
  }
  if (password.length < 8 || password.length > 20) {
    errors.push("Password must be between 8 and 20 characters.");
  }
  if (!passwordRegex.test(password)) {
    errors.push(
      "Password must include uppercase, lowercase, number, and special character.",
    );
  }
  if (password !== confirmPassword) {
    errors.push("Passwords do not match.");
  }
  if (!phoneRegex.test(phone)) {
    errors.push("Phone number must be exactly 10 digits.");
  }
  if (isNaN(age) || age < 18 || age > 122) {
    errors.push("Age must be a number between 18 and 122.");
  }

  if (gender === "") {
    errors.push("Gender is required.");
  }

  if (errors.length > 0) {
    for (const error of errors) {
      console.log(error);
      if (error.includes("Name")) {
        nameError.textContent = error;
      }
      if (error.includes("email")) {
        emailError.textContent = error;
      }
      if (error.includes("Password") && !error.includes("match")) {
        passwordError.textContent = error;
      }
      if (error.includes("match")) {
        confirmPasswordError.textContent = error;
      }
      if (error.includes("Phone")) {
        phoneError.textContent = error;
      }
      if (error.includes("Age")) {
        ageError.textContent = error;
      }
      if (error.includes("Gender")) {
        genderError.textContent = error;
      }
    }
  } else {
    alert("Form submitted successfully!");
  }
}

document
  .getElementById("validationForm")
  .addEventListener("submit", (event) => {
    event.preventDefault();
    validateForm();
  });
