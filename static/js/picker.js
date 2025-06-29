document.addEventListener("DOMContentLoaded", function () {
  // setup inputs
  const firstNameInput = document.getElementById("firstNameInput");
  const lastNameInput = document.getElementById("lastNameInput");
  const ghostNameInput = document.getElementById("ghostNameInput");

  // display box
  const ghostNameDisplay = document
    .getElementById("display")
    .querySelector(".card-body");
  const nameButtons = document.querySelectorAll(".btn-secondary");

  // init default ghost name
  let selectedGhostName = "";

  /**
   * Updates the display.
   * This could probably be a lot more efficient.
   *
   * @param {string} firstName the first name.
   * @param {string} lastName the last name.
   * @param {string} ghostName the ghost name.
   */
  function updateDisplay(firstName, lastName, ghostName = selectedGhostName) {
    if (firstName && lastName) {
      ghostNameDisplay.textContent = ghostName
        ? `${firstName} ${ghostName} ${lastName}`
        : `${firstName} ${lastName}`;
    } else if (firstName) {
      ghostNameDisplay.textContent = ghostName
        ? `${firstName} ${ghostName}`
        : firstName;
    } else if (lastName) {
      ghostNameDisplay.textContent = ghostName
        ? `${ghostName} ${lastName}`
        : lastName;
    } else if (ghostName) {
      ghostNameDisplay.textContent = ghostName;
    } else {
      ghostNameDisplay.textContent = "-";
    }
  }

  // first name input event listener
  firstNameInput.addEventListener("input", function () {
    const firstName = firstNameInput.value.trim();
    const lastName = lastNameInput.value.trim();
    updateDisplay(firstName, lastName);
  });

  // last name input event listener
  lastNameInput.addEventListener("input", function () {
    const firstName = firstNameInput.value.trim();
    const lastName = lastNameInput.value.trim();
    updateDisplay(firstName, lastName);
  });

  // purely cosmetic, but it sure does help with UX
  nameButtons.forEach((button) => {
    button.addEventListener("click", function () {
      nameButtons.forEach((btn) => {
        btn.classList.remove("btn-primary");
        btn.classList.add("btn-secondary");
      });

      button.classList.remove("btn-secondary");
      button.classList.add("btn-primary");

      // set the initialised value to the button text
      selectedGhostName = button.dataset.ghostName;
      ghostNameInput.value = selectedGhostName;

      // trim the values again just to make sure
      const firstName = firstNameInput.value.trim();
      const lastName = lastNameInput.value.trim();
      updateDisplay(firstName, lastName, selectedGhostName);
    });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("submitBtn").addEventListener("click", function () {
    var isValid = true;

    // Reset previous red borders
    document.getElementById("firstNameInput").style.borderColor = "";
    document.getElementById("lastNameInput").style.borderColor = "";
    document.getElementById("ghostNameInput").style.borderColor = "";

    // Get the form elements
    var firstName = document.getElementById("firstNameInput").value;
    var lastName = document.getElementById("lastNameInput").value;
    var ghostName = document.getElementById("ghostNameInput").value;

    // validator
    if (firstName === "") { isValid = false; }
    if (lastName === "") { isValid = false; }
    if (ghostName === "") { isValid = false; }

    // If all fields are valid, submit the form
    if (isValid) {
      document.getElementById("ghostNameForm").submit();
    } else {
      alert("Please fill in all required fields.");
    }
  });
});
