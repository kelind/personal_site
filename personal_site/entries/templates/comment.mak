##<%page args="form" />

<form action="/api/comment" id="comment" method="post">
  ${form.entry_id}
  <p>${form.name.label} ${form.name}</p>
  <p>${form.email.label} ${form.email}</p>
  <p>${form.body.label} ${form.body}</p>
  <button type="submit">Submit</button>
</form>
