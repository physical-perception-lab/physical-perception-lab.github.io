// Display featured projects on the overview page, sorted by year (most recent first)
document.addEventListener('DOMContentLoaded', function() {
  var dataEl = document.getElementById('featured-data');
  var grid = document.getElementById('featured-grid');
  if (!dataEl || !grid) return;

  var projects = JSON.parse(dataEl.textContent);

  // Shuffle using Fisher-Yates and pick 6
  for (var i = projects.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var tmp = projects[i];
    projects[i] = projects[j];
    projects[j] = tmp;
  }
  var selected = projects.slice(0, 6);

  // Sort selected by year descending (parse year from venue e.g. "CVPR, 2025")
  selected.sort(function(a, b) {
    var yearA = parseInt(a.venue.match(/\d{4}/)[0], 10);
    var yearB = parseInt(b.venue.match(/\d{4}/)[0], 10);
    return yearB - yearA;
  });

  var html = '';

  selected.forEach(function(p) {
    var mediaTag;
    if (p.img && (p.img.endsWith('.mp4') || p.img.endsWith('.m4v'))) {
      mediaTag = '<video class="card--featured__media" muted autoplay loop playsinline><source src="' + p.img + '" type="video/mp4"></video>';
    } else {
      mediaTag = '<img class="card--featured__media" src="' + p.img + '" alt="' + p.title.replace(/"/g, '&quot;') + '" loading="lazy">';
    }

    var link = p.project_page || p.pdf || '#';

    html += '<a class="card--featured" href="' + link + '" target="_blank" rel="noopener">';
    html += mediaTag;
    html += '<div class="card--featured__body">';
    html += '<div class="card--featured__title">' + p.title + '</div>';
    html += '<div class="card--featured__venue">' + p.venue + '</div>';
    html += '</div></a>';
  });

  grid.innerHTML = html;
});
