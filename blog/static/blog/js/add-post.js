// Load image preview EventListener
document.getElementById('id_image').onchange = function (event) {
  let reader = new FileReader();
  reader.onload = function () {
    let output = document.getElementById('imagePreview');
    output.src = reader.result;
    output.style.display = 'block';
  };
  reader.readAsDataURL(event.target.files[0]);
};

disableFormsSubmissionButton('addPostForm');