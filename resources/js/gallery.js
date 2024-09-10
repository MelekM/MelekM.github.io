document.querySelectorAll('.gallery a').forEach(anchor => {
    anchor.addEventListener('click', function(event) {
        event.preventDefault();
        const img = document.createElement('img');
        img.src = anchor.href;
        img.style.maxWidth = '90%';
        img.style.maxHeight = '90%';
        img.style.border = '2px solid #fff';
        img.style.borderRadius = '10px';

        const overlay = document.createElement('div');
        overlay.style.position = 'fixed';
        overlay.style.top = 0;
        overlay.style.left = 0;
        overlay.style.width = '100%';
        overlay.style.height = '100%';
        overlay.style.background = 'rgba(0, 0, 0, 0.8)';
        overlay.style.display = 'flex';
        overlay.style.alignItems = 'center';
        overlay.style.justifyContent = 'center';
        overlay.style.zIndex = 1000;

        overlay.appendChild(img);
        document.body.appendChild(overlay);

        overlay.addEventListener('click', function() {
            document.body.removeChild(overlay);
        });
    });
});
