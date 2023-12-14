// login.js
function login(event) {
    event.preventDefault();

    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;

    // Check credentials using the new API endpoint
    checkCredentials(email, password);
}




// signup 
   // signup 
// ...
$(document).ready(function () {
    $("#registration-form").submit(function (event) {
        event.preventDefault();

        var formData = {
            name: $("#name").val(),
            email: $("#email").val(),
            password: $("#password").val(),
            phoneNumber: $("#phoneNumber").val(),
            role: $("#role").val(),
            profession: $("#profession").val()
        };

        $.ajax({
            type: "POST",
            url: "/addUser",
            data: JSON.stringify(formData),
            contentType: "application/json;charset=UTF-8",
            success: function (response) {
                if (response.status === 'error') {
                    // Show error message
                    $("#error-message").text(response.message).show();
                    $("#success-message").hide();
                    // Clear form fields on error
                    clearFormFields();
                } else {
                    // Handle success response (e.g., show a success message)
                    $("#success-message").text(response.message).show();
                    $("#error-message").hide();
                    // Clear form fields on success if needed
                    clearFormFields();
                }
            },
            
            error: function (error) {
                // Handle error response
                $("#error-message").text(error.responseJSON.message).show();
                $("#success-message").hide();
                // Clear form fields on error
                clearFormFields();
            }
           
        });
        $("#name, #email, #password, #phoneNumber, #role, #profession").click(function () {
            // Hide error messages when a field is clicked
            $("#error-message").hide();
            $("#success-message").hide();
        });
    
    });
});

function clearFormFields() {
    // Clear all form fields
    $("#name").val('');
    $("#email").val('');
    $("#password").val('');
    $("#phoneNumber").val('');
    $("#role").val('');
    $("#profession").val('');
}






