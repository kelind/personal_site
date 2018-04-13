<%inherit file="base.mak" />

<%block name="title">Tags</%block>

<%block name="maincontent">

  <article id="tagblock">
  <h1>Tags</h1>
  <p>Click a tag name to retrieve all entries it's been used on. If you subscribe to a tag, you'll receive an e-mail whenever a new entry with that tag is posted.</p>

  <ul>
  % for tag in tags:
    % if tag[2] == 1:
      <li><a href="${url_for('entries.tag_details', slug=tag.slug)}">${tag.tagname}</a> - ${tag[2]} use (<a href="${url_for('mailing.subscribe', slug=tag.slug)}">Subscribe</a>)</li>
    % else:
      <li><a href="${url_for('entries.tag_details', slug=tag.slug)}">${tag.tagname}</a> - ${tag[2]} uses (<a href="${url_for('mailing.subscribe', slug=tag.slug)}">Subscribe</a>)</li>
    % endif
  % endfor
  </ul>
  </article>

</%block>
