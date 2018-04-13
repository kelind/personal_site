<%inherit file="base.mak" />

<%block name="title">Confirmation Succeeded</%block>

<%block name="maincontent">

  <article>

  % if action == 'subscribe':

  <p>You have successfully subscribed to ${tag}. Watch your e-mail for future updates!</p>

  % else:

    <p>You have been successfully unsubscribed from ${tag}.</p>

  % endif

  <a href="${url_for('entries.index')}">Return to the blog.</a>

  </article>

</%block>
