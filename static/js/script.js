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