/* Functions */
const attachBtnUploadEvt = () => {
  document.getElementById('uploadPictureBtn').addEventListener('click', function () {
    document.getElementById('uploadPictureInput').click();
  });
}

/* Events */

// After profile picture swap from htmx we attach the event again to the uploadPictureBtn
document.addEventListener('htmx:afterSwap', (evt) => {
  if (evt.detail.elt.id == 'authorProfilePictureContainer') {
    attachBtnUploadEvt();
  }
});


/* Init calls */
attachBtnUploadEvt();
disableFormsSubmissionButtonHtmx('modifyAuthoForm');