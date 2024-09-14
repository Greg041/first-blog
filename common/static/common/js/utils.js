// Disable form submit buttons and shows a spinner with Loading text
function disableFormsSubmissionButton(formElementId) {
  const form = document.querySelector(`#${formElementId}`);
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const submit = form.querySelector('button[type="submit"]');
    submit.disabled = true;
    submit.querySelector('span').textContent = 'Cargando';
    submit.querySelector('.spinner-border').classList.remove('visually-hidden');
    form.submit();
  });
}

// Same as disableFormsSubmissionButton but adapted to use with htmx form submissions.
function disableFormsSubmissionButtonHtmx(formElementId) {
  let buttonInnerHTML;

  document.body.addEventListener('htmx:beforeRequest', (evt) => {
    // We check the element that triggered the request is a form
    if (evt.detail.elt instanceof HTMLFormElement && evt.detail.elt.id == formElementId) {
      const form = evt.detail.elt;
      const submit = form.querySelector('button[type="submit"]')
      submit.disabled = true;
      // We save the innerHTML from the button to restore it after
      // the request is finished
      buttonInnerHTML = submit.querySelector('span').textContent;
      // Show the loading interface in the button
      submit.querySelector('span').textContent = 'Cargando';
      submit.querySelector('.spinner-border').classList.remove('visually-hidden');
    }
  });

  document.body.addEventListener('htmx:afterRequest', (evt) => {
    // We check the element that triggered the request is a form
    if (evt.detail.elt instanceof HTMLFormElement && evt.detail.elt.id == formElementId) {
      const form = evt.detail.elt;
      const submit = form.querySelector('button[type="submit"]')
      submit.disabled = false;
      // We restore the original textContent from the button
      submit.querySelector('span').textContent = buttonInnerHTML;
      submit.querySelector('.spinner-border').classList.add('visually-hidden');
    }
  })
}