<%page args="entry" />

<p class="inline-partner double-space">Tags:</p> <ul class="taglist">
  % for index, tag in enumerate(entry.tags):
    % if not index + 1 == len(entry.tags):
      <li><a href="${url_for('entries.tag_details', slug=tag.slug)}">${tag.tagname}</a>, </li> 
    % else:
          <li><a href="${url_for('entries.tag_details', slug=tag.slug)}">${tag.tagname}</a></li>
   % endif
 % endfor
</ul>

