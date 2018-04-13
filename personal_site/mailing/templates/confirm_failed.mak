<%inherit file="base.mak" />

<%block name="title">Confirmation Failed</%block>

<%block name="maincontent">

<article>
% if reason == 'disabled':
  <p>E-mail subscription is currently disabled. Please try again later.</p>
% else:
  <p>There was a problem with the security token or it has expired. Please try subscribing or unsubscribing again to generate another confirmation e-mail.</p>
% endif
<p><a href="${url_for('entries.index')}">Return to the blog.</a></p>
</article>

</%block>
