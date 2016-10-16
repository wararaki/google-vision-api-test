$(function(){
  // check box checker


  // button click event
  $('#google-vis').click(function(){
    // get file
    var file = document.querySelector('input[type=file]').files[0];
    var reader = new FileReader();

    // set onload event
    reader.onload = (function(theFile){
      return function(e) {
        // api request
        var request_data = {
          'image': e.target.result,
          'checks': []
        };

        // ajax request
        $.ajax({
          url: '/api/classify',
          type: 'POST',
          contentType: 'application/json',
          dataType: "json",
          data: JSON.stringify(request_data)
        }).done(function(response){
          console.log(response);
        }).fail(function(response){
          console.log(response);
        });

        return;
      };
    })(file);

    // convert base64
    if(file){
      reader.readAsDataURL(file);
    } else {
      alert('empty!');
    }
  });
});
