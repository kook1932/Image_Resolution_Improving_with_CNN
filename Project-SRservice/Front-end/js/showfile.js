/*  ==========================================
    SHOW UPLOADED IMAGE
* ========================================== */
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#imageResult')
                .attr('src', e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
}

$(function () {
    $('#upload').on('change', function () {
        readURL(input);
    });
});

/*  ==========================================
    SHOW UPLOADED IMAGE NAME
* ========================================== */
var input = document.getElementById( 'upload' );
var infoArea = document.getElementById( 'upload-label' );

input.addEventListener( 'change', showFileName );
function showFileName( event ) {
  var input = event.srcElement;
  var fileName = input.files[0].name;
  infoArea.textContent = 'File name: ' + fileName;
}

/*  ==========================================
	SHOW EMAIL
* ========================================== */


var email_input=document.getElementById( 'email' );
email_input.addEventListener( 'click', emailWrite );
function emailWrite( event ) {
  var input = event.srcElement;
  if (input.value=='Insert email'){
    input.value = '';
  }


}
email_input.addEventListener('blur',function(event){
  var input = event.srcElement;
  if (input.value==''){
    input.value = 'Insert email';
  }

})
