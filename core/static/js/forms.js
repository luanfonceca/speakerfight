$(function () {
  tinymce.init({
    selector: "textarea",
    menubar: false,
    skin: 'light',
    plugins: 'link paste preview textcolor',
    toolbar: "bold italic underline forecolor | alignleft aligncenter alignright | link unlink | undo redo removeformat | formatselect fontsizeselect pastetext | preview",
    body_class: 'form-control',
  });
});
