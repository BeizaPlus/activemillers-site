/* Contact CTA: "Yes, I want to know more" -> reveal email capture -> post to
   local capture endpoint. Global widget, one instance per page (IDs, not
   classes, since there's only ever one contact section per article).

   HTML structure expected:
   <button type="button" class="contact-icon partner-cta secondary" id="learnMoreYesBtn">Yes, I want to know more</button>
   <form class="contact-email-form" id="learnMoreForm">
     <input type="email" id="learnMoreEmail" placeholder="you@email.com" required>
     <button type="submit">Send it to me</button>
   </form>
   <p class="contact-email-success" id="learnMoreSuccess">...</p>

   Set data-source on #learnMoreForm to tag the lead by article slug, e.g.
   <form ... data-source="wallenberg-syndrome">. Defaults to the page filename.
*/
(function () {
  var yesBtn = document.getElementById('learnMoreYesBtn');
  var form = document.getElementById('learnMoreForm');
  if (!yesBtn || !form) return;

  var emailInput = document.getElementById('learnMoreEmail');
  var success = document.getElementById('learnMoreSuccess');
  var source = form.dataset.source || location.pathname.split('/').pop().replace('.html', '');

  yesBtn.addEventListener('click', function () {
    yesBtn.hidden = true;
    form.classList.add('visible');
    if (emailInput) emailInput.focus();
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var email = emailInput.value.trim();
    if (!email) return;
    fetch('http://localhost:8761/subscribe', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email, source: source, list: 'article-pdf-request' })
    }).then(function (r) {
      if (r.ok) {
        form.style.display = 'none';
        success.classList.add('visible');
      } else {
        throw new Error('capture server error');
      }
    }).catch(function () {
      success.textContent = 'Signup server offline right now. Email steven.oppong@gmail.com and we\'ll send it directly.';
      success.classList.add('visible');
    });
  });
})();
