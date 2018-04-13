<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title><%block name="title">Home</%block> - Before I Sleep</title>
  <link href="https://fonts.googleapis.com/css?family=Calligraffitti" rel="stylesheet" type="text/css"> 
  <link type="text/css" rel="stylesheet" href="${url_for('static', filename="global.css")}" />
  <%block name="resource">
  % if resources:
    % for resource in resources:
      % if resource.endswith('.js'):
        <script type="text/javascript" src="${url_for('static', filename=resource)}"></script>
      % elif resource.endswith('.css'):
        <link type="text/css" rel="stylesheet" href="${url_for('static', filename=resource)}" />
      % endif
    % endfor
  % endif
  </%block>
</head>
<body>
  <div id="main">
    <header id="mainheader">
      <div id="banner">&nbsp;</div>
      <h1><a href="${url_for('homepage')}">Before I Sleep</a></h1>
      <%include file="nav.mak" args="nav=nav" />
    </header>
    <div id="content">
      <%block name="maincontent">
        <article id="maincontent">
          <h1>${content_title}</h1>
          ${content}
        </article>
      </%block>
    </div>
    <footer id="mainfooter">
      <%include file="footer.mak" />
    </footer>
  </div>
</body>
</html>
