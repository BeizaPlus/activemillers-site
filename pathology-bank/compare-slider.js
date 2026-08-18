/* Before/After comparison slider — finds every .compare-container on the page and wires it up.
   Load this file on any page that has a compare slider. No IDs needed; uses classes + data attributes.

   HTML structure expected:
   <div class="compare-container" data-label-before="Sketch" data-label-after="Final">
     <span class="compare-label compare-label-before">Sketch</span>
     <span class="compare-label compare-label-after">Final</span>
     <div class="compare-layer">
       <img src="before.jpg" alt="Before" draggable="false">
     </div>
     <div class="compare-layer compare-top">
       <div class="compare-layer">
         <img src="after.jpg" alt="After" draggable="false">
       </div>
     </div>
     <div class="compare-divider"></div>
     <div class="compare-handle" role="slider" tabindex="0">
       <span class="compare-handle-circle">
         <svg class="compare-handle-arrows" viewBox="0 0 24 24"><path fill="currentColor" d="M10 8l-4 4 4 4V8zm4 8l4-4-4-4v8z"/></svg>
       </span>
     </div>
   </div>
*/
(function () {
  var containers = document.querySelectorAll('.compare-container');
  containers.forEach(function (container) {
    if (container.dataset.wired) return;
    container.dataset.wired = '1';

    var topLayer = container.querySelector('.compare-top');
    var divider  = container.querySelector('.compare-divider');
    var handle   = container.querySelector('.compare-handle');
    if (!topLayer || !divider || !handle) return;

    var dragging = false;

    function setPosition(percent) {
      percent = Math.max(2, Math.min(98, percent));
      var leftPct = percent.toFixed(1) + '%';
      var rightClip = (100 - percent).toFixed(1) + '%';
      topLayer.style.clipPath = 'inset(0px ' + rightClip + ' 0px 0px)';
      divider.style.left = leftPct;
      divider.style.transform = 'translateX(-50%)';
      handle.style.left = leftPct;
      handle.style.transform = 'translateX(-50%)';
      handle.setAttribute('aria-valuenow', Math.round(percent));
    }

    function getEventX(e) {
      return e.touches ? e.touches[0].clientX : e.clientX;
    }

    function onStart(e) {
      e.preventDefault();
      dragging = true;
      document.body.style.cursor = 'ew-resize';
    }

    function onMove(e) {
      if (!dragging) return;
      var rect = container.getBoundingClientRect();
      var x = getEventX(e);
      var percent = ((x - rect.left) / rect.width) * 100;
      setPosition(percent);
    }

    function onEnd() {
      dragging = false;
      document.body.style.cursor = '';
    }

    handle.addEventListener('mousedown', onStart);
    document.addEventListener('mousemove', onMove);
    document.addEventListener('mouseup', onEnd);

    handle.addEventListener('touchstart', onStart, { passive: false });
    document.addEventListener('touchmove', onMove, { passive: false });
    document.addEventListener('touchend', onEnd);

    handle.addEventListener('keydown', function (e) {
      var current = parseInt(handle.getAttribute('aria-valuenow')) || 50;
      if (e.key === 'ArrowLeft'  || e.key === 'Left')  { e.preventDefault(); setPosition(current - 5); }
      if (e.key === 'ArrowRight' || e.key === 'Right') { e.preventDefault(); setPosition(current + 5); }
    });

    var start = parseInt(container.dataset.start, 10);
    setPosition(isNaN(start) ? 50 : start);
  });
})();
