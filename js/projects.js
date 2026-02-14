// Topic filtering on the projects page
document.addEventListener('DOMContentLoaded', function() {
  var filterBar = document.getElementById('filter-bar');
  if (filterBar) {
    var buttons = filterBar.querySelectorAll('.filter__btn');
    var cards = document.querySelectorAll('.card--project');
    var yearDividers = document.querySelectorAll('.year-divider');

    buttons.forEach(function(btn) {
      btn.addEventListener('click', function() {
        // Update active button
        buttons.forEach(function(b) { b.classList.remove('filter__btn--active'); });
        btn.classList.add('filter__btn--active');

        var topic = btn.getAttribute('data-topic');

        // Show/hide cards
        cards.forEach(function(card) {
          if (topic === 'all') {
            card.style.display = '';
          } else {
            var topics = card.getAttribute('data-topics') || '';
            if (topics.split(',').indexOf(topic) !== -1) {
              card.style.display = '';
            } else {
              card.style.display = 'none';
            }
          }
        });

        // Show/hide year dividers based on whether any cards in that year are visible
        yearDividers.forEach(function(divider) {
          var year = divider.getAttribute('data-year');
          var hasVisible = false;
          cards.forEach(function(card) {
            if (card.getAttribute('data-year') === year && card.style.display !== 'none') {
              hasVisible = true;
            }
          });
          divider.style.display = hasVisible ? '' : 'none';
        });
      });
    });
  }

  // Prospective students toggle
  var toggle = document.getElementById('prospective-toggle');
  var content = document.getElementById('prospective-content');
  var arrow = document.getElementById('prospective-arrow');
  if (toggle && content && arrow) {
    toggle.addEventListener('click', function() {
      content.classList.toggle('prospective__content--open');
      arrow.classList.toggle('prospective__arrow--open');
    });
  }
});
