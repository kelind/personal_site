<%inherit file="base.mak" />

<%block name="title">Create Entry</%block>

<%block name="maincontent">

  <h1>Create New Entry</h1>

  <form action="${url_for('entries.create')}" id="create_entry" method="post">

    ${form.csrf_token}

    % for field in form:
      % if not field.id == 'csrf_token':
        <div class="form-group">
          ${field.label}
          ${field}
        </div>
      % endif
    % endfor

    <div class="form-group">
      <button type="submit">Create</button>
      <a class="button" href="${url_for('entries.index')}">Cancel</a>
    </div>
  </form>

</%block>
