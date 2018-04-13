<%inherit file="base.mak" />

<%block name="title">Subscribe to ${tag.tagname}</%block>

<%block name="maincontent">

<article>
  <h1>Subscribe to ${tag.tagname}</h1>

  <p>Enter your e-mail address below to receive an e-mail whenever a post with the tag "${tag.tagname}" is posted to the blog. You can unsubscribe at any time.</p>

  <form action="${url_for('mailing.subscribe', slug=tag.slug)}" id="subscribe" method="post">

    % for field in form:
      % if not field.id == "csrf_token":
        ${field.label} ${field}
      % endif
    % endfor

    <button type="submit">Subscribe</button>
  </article>

</form>

</%block>
