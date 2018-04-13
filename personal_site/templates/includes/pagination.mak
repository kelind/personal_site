<nav class="pagination">
  <ul>
   % if not object_list.has_prev:
     <li class="disabled">
  % else:
    <li>
  % endif
      % if object_list.has_prev:
        <a href="./?page=${object_list.prev_num}">&laquo;</a>
      % else:
        <a href="#">&laquo;</a>
      % endif
    </li>
    % for page in object_list.iter_pages():
        <li>
          % if page:
            % if page == object_list.page:
              <a class="active" href="./?page=${page}">Page ${page}</a>
            % else:
              <a href="./?page=${page}">Page ${page}</a>
            % endif
          % else:
              <a class="disabled">...</a>
          % endif
        </li>
    % endfor
    % if not object_list.has_next:
      <li class="disabled">
    % else:
      <li>
    % endif
      % if object_list.has_next:
        <a href="./?page=${object_list.next_num}">&raquo;</a>
      % else:
        <a href="#">&raquo;</a>
      % endif
    </li>
  </ul>
</nav>
