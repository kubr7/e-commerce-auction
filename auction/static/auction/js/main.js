function toggleDropdown() {
     var optionsContainer = document.querySelector('.options-container');
     optionsContainer.style.display = optionsContainer.style.display === 'none' ? 'flex' : 'none';
}

// Close the dropdown if the user clicks outside of it
document.addEventListener('click', function (event) {
     var customSelect = document.getElementById('brand');
     if (!customSelect.contains(event.target)) {
          var optionsContainer = document.querySelector('.options-container');
          optionsContainer.style.display = 'none';
     }
});