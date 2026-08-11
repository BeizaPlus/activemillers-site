/* Click-to-play video — finds every .video-figure on the page and wires it up.
   Load this file on any page that has a video. No IDs needed; uses classes only.

   HTML structure expected:
   <div class="step-figure video-figure">
     <video playsinline preload="none" muted poster="thumb.jpg">
       <source src="videos/clip.mp4" type="video/mp4">
     </video>
     <button class="video-play-btn" aria-label="Play video">
       <svg viewBox="0 0 24 24" fill="currentColor"><path d="M6 4v16a1 1 0 0 0 1.524 .852l13 -8a1 1 0 0 0 0 -1.704l-13 -8a1 1 0 0 0 -1.524 .852z" /></svg>
     </button>
   </div>
*/
(function () {
  var figures = document.querySelectorAll('.video-figure');
  figures.forEach(function (figure) {
    if (figure.dataset.wired) return;
    var video = figure.querySelector('video');
    var btn = figure.querySelector('.video-play-btn');
    if (!video || !btn) return;
    figure.dataset.wired = '1';

    function toggle() {
      if (video.paused) { video.play(); } else { video.pause(); }
    }

    btn.addEventListener('click', function (e) { e.stopPropagation(); toggle(); });
    video.addEventListener('click', toggle);
    video.addEventListener('play', function () { btn.classList.add('hidden'); });
    video.addEventListener('pause', function () { btn.classList.remove('hidden'); });
    video.addEventListener('ended', function () { btn.classList.remove('hidden'); });
  });
})();
