---
layout: page
lang: en
title: "Contact"
permalink: /en/contact/
---

<h2>Contact</h2>

<p>Have a question, a suggestion or a problem? Write to me — I'll reply as soon as possible.</p>

<form action="https://formspree.io/f/mpzewgzq" method="POST" class="form">
  <input type="email" name="email" placeholder="Your email address" required>
  <textarea name="content" rows="6" placeholder="Your message" required></textarea>
  <input type="hidden" name="_next" value="{{ site.url }}/en/thanks/">
  <input type="hidden" name="_subject" value="Message from appseven.fr">
  <input type="text" name="_gotcha" style="display:none">
  <button type="submit" class="button">Send</button>
</form>
