function validateForm() {
    const form = document.getElementById("registrationForm");
    const name = form.name.value.trim();
    const email = form.email.value.trim();
    const mobile = form.mobile.value.trim();
    const username = form.username.value.trim();
    const password = form.password.value;
    const postalCode = form.postalCode.value.trim();
    const photo = form.photo.value;

    // Clear previous error messages
    const errorElements = document.querySelectorAll(".error");
    errorElements.forEach((el) => el.remove());

    let isValid = true;

    // Name validation
    if (name.length < 2) {
      showError(form.name, "Name must be at least 2 characters long");
      isValid = false;
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      showError(form.email, "Please enter a valid email address");
      isValid = false;
    }

    // Mobile number validation
    const mobileRegex = /^[0-9]{10}$/;
    if (!mobileRegex.test(mobile)) {
      showError(form.mobile, "Please enter a valid 10-digit mobile number");
      isValid = false;
    }

    // Username validation
    if (username.length < 4) {
      showError(
        form.username,
        "Username must be at least 4 characters long"
      );
      isValid = false;
    }

    // Password validation
    if (password.length < 8) {
      showError(
        form.password,
        "Password must be at least 8 characters long"
      );
      isValid = false;
    }

    // Photo validation
    if (!photo) {
      showError(form.photo, "Please select a photo");
      isValid = false;
    }

    // Additional field validations
    if (!validateRequiredField(form.street, "Street Name")) isValid = false;
    if (!validateRequiredField(form.colony, "Colony/Locality"))
      isValid = false;
    if (!validateRequiredField(form.city, "City")) isValid = false;
    if (!validateRequiredField(form.state, "State")) isValid = false;
    if (!validateRequiredField(form.country, "Country")) isValid = false;

    return isValid;
  }

  function validateRequiredField(field, fieldName) {
    if (field.value.trim() === "") {
      showError(field, `${fieldName} is required`);
      return false;
    }
    return true;
  }

  function showError(input, message) {
    const error = document.createElement("div");
    error.className = "error";
    error.textContent = message;
    input.parentNode.insertBefore(error, input.nextSibling);
  }

  // Add event listener for form submission
  document
    .getElementById("registrationForm")
    .addEventListener("submit", function (event) {
      if (!validateForm()) {
        event.preventDefault(); // Prevent form submission if validation fails
      }
    });