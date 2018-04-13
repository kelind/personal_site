<%namespace name="util" file="util/error.mak" />

<%inherit file="base.mak" />

<%block name="title">Log In</%block>

<%block name="maincontent">

<h1>Log In</h1>

<form action="${url_for('login', next=request.args.get('next', ''))}" method="post">

  ${form.name.label} ${form.name}
  <%util:error field="${form.name}" />

  ${form.password.label} ${form.password}
  ${form.remember_me} ${form.remember_me.label} 

  <button type="submit">Log In</button>
  <a class="btn" href="${url_for('homepage')}">Cancel</a>

</form>

</%block>
