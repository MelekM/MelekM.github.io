function includeHTML() {
    var elements = document.querySelectorAll('[data-include]');

    elements.forEach(function(el) {
        var file = el.getAttribute('data-include');

        if (file) {
            fetch(file)
                .then(response => response.text())
                .then(data => {
                    el.innerHTML = data;
                    el.removeAttribute('data-include');
                    // Call includeHTML recursively to handle nested includes
                    includeHTML();
                })
                .catch(error => console.error('Error loading file:', error));
        }
    });
}

document.addEventListener('DOMContentLoaded', includeHTML);
