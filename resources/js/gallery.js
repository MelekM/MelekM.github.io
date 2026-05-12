(() => {
  const modal = document.getElementById('photo-modal');

  if (!modal) {
    return;
  }

  const image = modal.querySelector('[data-photo-image]');
  const title = modal.querySelector('[data-photo-title]');
  const caption = modal.querySelector('[data-photo-caption]');
  const counter = modal.querySelector('[data-photo-counter]');
  const closeTargets = Array.from(modal.querySelectorAll('[data-close-modal]'));
  const prevButton = modal.querySelector('[data-photo-prev]');
  const nextButton = modal.querySelector('[data-photo-next]');

  const links = Array.from(document.querySelectorAll('.photography .gallery > figure > a'));
  const items = links.map((link) => {
    const thumb = link.querySelector('img');
    const figure = link.closest('figure');
    const captionText = figure?.querySelector('figcaption')?.innerText?.trim() || '';

    if (thumb) {
      const fullSrc = link.href;
      thumb.src = fullSrc;
      thumb.loading = 'lazy';
      thumb.decoding = 'async';
      thumb.srcset = '';
    }

    return {
      href: link.href,
      alt: thumb?.alt || link.dataset.title || 'Photography preview',
      title: link.dataset.title || thumb?.alt || 'Photography preview',
      captionText
    };
  });

  if (!items.length) {
    return;
  }

  let activeIndex = 0;
  let previousFocus = null;

  function setActiveItem(index) {
    activeIndex = (index + items.length) % items.length;
    const item = items[activeIndex];

    image.src = item.href;
    image.alt = item.alt;
    if (title) {
      title.textContent = item.title;
    }
    caption.textContent = item.captionText;
    counter.textContent = `${activeIndex + 1} of ${items.length}`;
  }

  function openModal(index) {
    previousFocus = document.activeElement;
    setActiveItem(index);
    modal.hidden = false;
    modal.setAttribute('aria-hidden', 'false');
    document.body.classList.add('modal-open');
    closeTargets[0]?.focus();
  }

  function closeModal() {
    modal.hidden = true;
    modal.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('modal-open');
    if (previousFocus && typeof previousFocus.focus === 'function') {
      previousFocus.focus();
    }
  }

  function move(delta) {
    setActiveItem(activeIndex + delta);
  }

  document.addEventListener('click', (event) => {
    const link = event.target.closest('.photography .gallery > figure > a');
    if (!link) {
      return;
    }

    const index = links.indexOf(link);
    if (index === -1) {
      return;
    }

    event.preventDefault();
    openModal(index);
  });

  closeTargets.forEach((target) => {
    target.addEventListener('click', closeModal);
  });

  prevButton?.addEventListener('click', () => move(-1));
  nextButton?.addEventListener('click', () => move(1));

  modal.addEventListener('click', (event) => {
    if (event.target === modal) {
      closeModal();
    }
  });

  document.addEventListener('keydown', (event) => {
    if (modal.hidden) {
      return;
    }

    if (event.key === 'Escape') {
      closeModal();
    } else if (event.key === 'ArrowLeft') {
      move(-1);
    } else if (event.key === 'ArrowRight') {
      move(1);
    }
  });
})();
