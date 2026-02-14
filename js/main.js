// Mobile nav toggle
document.addEventListener('DOMContentLoaded', function() {
  var hamburger = document.querySelector('.nav__hamburger');
  var links = document.querySelector('.nav__links');
  if (hamburger && links) {
    hamburger.addEventListener('click', function() {
      links.classList.toggle('nav__links--open');
    });
    // Close nav when clicking a link
    links.querySelectorAll('.nav__link').forEach(function(link) {
      link.addEventListener('click', function() {
        links.classList.remove('nav__links--open');
      });
    });
  }
});

// Toggle bibtex blocks
function toggleblock(blockId) {
  var block = document.getElementById(blockId);
  if (!block) return;
  if (block.style.display === 'none' || block.style.display === '') {
    block.style.display = 'block';
  } else {
    block.style.display = 'none';
  }
}
