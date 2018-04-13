<%! from markdown import markdown %>

<%inherit file="base.mak" />

<%block name="title">${entry.title}</%block>

<%block name="maincontent">

<article id="blog-entry">
  <h1>${entry.title}</h1>
  <p><i>Published ${format_date(entry.created_timestamp)}</i></p>
  ${markdown(entry.body)}

  % if entry.tags:
    <%include file="taglist.mak" />
  % endif

  ##<%include file="comment.mak" />
</article>

</%block>
