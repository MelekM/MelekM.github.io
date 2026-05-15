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
                    applySharedUI();
                    // Call includeHTML recursively to handle nested includes
                    includeHTML();
                })
                .catch(error => console.error('Error loading file:', error));
        }
    });
}

function normalizePath(path) {
    if (!path || path === "/") {
        return "/index.html";
    }

    return path.endsWith("/") ? `${path}index.html` : path;
}

function applySharedUI() {
    const currentPath = normalizePath(window.location.pathname);

    document.querySelectorAll('nav .nav-links a').forEach(function(link) {
        const linkPath = normalizePath(new URL(link.href, window.location.origin).pathname);
        const isActive = currentPath === linkPath;
        link.classList.toggle('is-active', isActive);

        if (isActive) {
            link.setAttribute('aria-current', 'page');
        } else {
            link.removeAttribute('aria-current');
        }

        link.addEventListener('click', function() {
            const navLinks = document.querySelector('.nav-links');
            if (navLinks) {
                navLinks.classList.remove('active');
            }
        });
    });

    document.querySelectorAll('[data-year]').forEach(function(node) {
        node.textContent = new Date().getFullYear();
    });
}

document.addEventListener('DOMContentLoaded', function() {
    includeHTML();
    applySharedUI();
});
