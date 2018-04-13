<%def name="error(field)">
    % if field.errors:
      <ul class="error">
        % for err in field.errors:
          <li>${err}</li>
        % endfor
      </ul>
    % endif
</%def>

