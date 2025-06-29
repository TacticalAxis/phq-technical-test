document.addEventListener('DOMContentLoaded', function() {
    const firstNameInput = document.getElementById('firstNameInput');
    const lastNameInput = document.getElementById('lastNameInput');
    const ghostNameInput = document.getElementById('ghostNameInput');
    const ghostNameDisplay = document.getElementById('display').querySelector('.card-body');
    const nameButtons = document.querySelectorAll('.btn-secondary');
    let selectedGhostName = '';

    function updateDisplay(firstName, lastName, ghostName = selectedGhostName) {
        if (firstName && lastName) {
            ghostNameDisplay.textContent = ghostName ? `${firstName} ${ghostName} ${lastName}` : `${firstName} ${lastName}`;
        } else if (firstName) {
            ghostNameDisplay.textContent = ghostName ? `${firstName} ${ghostName}` : firstName;
        } else if (lastName) {
            ghostNameDisplay.textContent = ghostName ? `${ghostName} ${lastName}` : lastName;
        } else if (ghostName) {
            ghostNameDisplay.textContent = ghostName;
        } else {
            ghostNameDisplay.textContent = '-';
        }
    }

    firstNameInput.addEventListener('input', function() {
        const firstName = firstNameInput.value.trim();
        const lastName = lastNameInput.value.trim();
        updateDisplay(firstName, lastName);
    });

    lastNameInput.addEventListener('input', function() {
        const firstName = firstNameInput.value.trim();
        const lastName = lastNameInput.value.trim();
        updateDisplay(firstName, lastName);
    });

    nameButtons.forEach(button => {
        button.addEventListener('click', function() {
            nameButtons.forEach(btn => {
                btn.classList.remove('btn-primary');
                btn.classList.add('btn-secondary');
            });
            
            button.classList.remove('btn-secondary');
            button.classList.add('btn-primary');
            
            selectedGhostName = button.dataset.ghostName;
            ghostNameInput.value = selectedGhostName;
            const firstName = firstNameInput.value.trim();
            const lastName = lastNameInput.value.trim();
            updateDisplay(firstName, lastName, selectedGhostName);
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('submitBtn').addEventListener('click', function () {
            var isValid = true;
    
    // Reset previous red borders
    document.getElementById('firstNameInput').style.borderColor = '';
    document.getElementById('lastNameInput').style.borderColor = '';
    document.getElementById('ghostNameInput').style.borderColor = '';

    // Get the form elements
    var firstName = document.getElementById('firstNameInput').value;
    var lastName = document.getElementById('lastNameInput').value;
    var ghostName = document.getElementById('ghostNameInput').value;

    // Check if first name is empty
    if (firstName === "") {
        document.getElementById('firstNameInput').style.borderColor = 'red';
        isValid = false;
    }

    // Check if last name is empty
    if (lastName === "") {
        document.getElementById('lastNameInput').style.borderColor = 'red';
        isValid = false;
    }

    // Check if ghost name is selected
    if (ghostName === "") {
        document.getElementById('ghostNameInput').style.borderColor = 'red';
        isValid = false;
    }

    // If all fields are valid, submit the form
    if (isValid) {
        document.getElementById('ghostNameForm').submit();
    } else {
        alert("Please fill in all required fields.");
    }
});
});