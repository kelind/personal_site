<%inherit file="base.mak" />

<%block name="title">Confirm Subscription</%block>

<%block name="maincontent">

<article>
  <p>A confirmation e-mail has been sent to ${email}. To complete your subscription, please click the link in the message you receive.</p>
  <p><a href="${url_for('entries.index')}">Return to the blog.</a></p>
</article>

</%block>
