<%! from markdown import markdown %>

<%inherit file="base.mak" />

<%block name="title">${page_title}</%block>

<%block name="maincontent">

% if not page_title == 'Home':
  <h1 class="center">${page_title}</h1>
% endif

% for entry in object_list.items:
  <article class="entry-summary">
    <h1><a href="${url_for('entries.detail', slug=entry.slug)}">${entry.title}</a></h1>
    % if entry.img:
      <img src="${url_for('static', filename='/'.join(entry.img.split('/')[-3:]))}" alt="" class="entry-summary-img" />
    % endif
    <p><i>Posted ${format_date(entry.created_timestamp)}</i></p>
    <p class="double-space">${markdown(entry.summary)}</p>
    % if entry.body:
      <p><i><a href="${url_for('entries.detail', slug=entry.slug)}">Read more...</a></i></p>
    % endif
    <nav id="tags-comments">
    % if entry.tags:
      <%include file="taglist.mak" args="entry=entry" />
    % endif
    <p class="right-float">Comments: 0</p>
    </nav>
  </article>
% endfor

<%include file="includes/pagination.mak" />

</%block>
