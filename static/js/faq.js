$(document).ready(function () {

    $("#faq-form").submit(function (event) {
        event.preventDefault();

        var formData = {
            question: $("#question").val(),
            answer: $("#answer").val(),
        };

        $.ajax({
            type: "POST",
            url: "/addfaq",
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

                    // Reload the page after successful submission
                    location.reload();
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

        // Hide error messages when a field is clicked
        $("#question, #answer").click(function () {
            $("#error-message").hide();
            $("#success-message").hide();
        });
    });

    function clearFormFields() {
        // Clear all form fields
        $("#question").val('');
        $("#answer").val('');
    }
});
