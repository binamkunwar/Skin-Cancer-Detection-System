$(document).ready(function () {
    $('.image-selection').hide();
    $('.loader').hide();
    $('#result').hide();
    $('#doctors').hide(); // Hide doctors initially

    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    $('#imageUpload').change(function () {
        var input = this;
        var img = $('#imagePreview')[0];
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                img.src = e.target.result;
                $('.image-selection').show();
                $('#btn-predict').show();
                $('#result').text('');
                $('#result').hide();
                $('#doctors').hide(); // Hide doctors when a new prediction is made
            };

            reader.readAsDataURL(input.files[0]);
        }
    });

    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling the API
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').text('Result: ' + data);
                console.log('Success!!');
                if (data.toLowerCase() === 'no skin cancer') {
                    // If the result is 'No Skin Cancer', fetch and display dermatologists
                    fetchDoctors('Dermatologist');
                } else if (data.toLowerCase() === 'skin cancer') {
                    // If the result is 'Skin Cancer', fetch and display cancer specialists
                    fetchDoctors('Cancer Specialist');
                } else {
                    console.log('Unknown result:', data);
                }
            },
            error: function () {
                // Handle errors here
                console.log('Error occurred during prediction.');
            }
        });
    });

    function fetchDoctors(specialization) {
        // Fetch doctors from the add_doctor table based on specialization
        $.ajax({
            type: 'GET',
            url: '/fetchDoctors/' + specialization,
            success: function (doctors) {
                // Process the fetched doctors
                console.log('Doctors:', doctors);
                // Display doctors or perform additional actions
                updateDoctorList(doctors);
            },
            error: function () {
                // Handle errors here
                console.log('Error occurred during doctor fetch.');
            }
        });
    }

    function updateDoctorList(doctors) {
        // Update the doctors section in the DOM
        $('#doctors').show(); // Show doctors section
        var doctorsList = $('#doctors-list');
        doctorsList.empty(); // Clear previous entries

        // Append each doctor's information
        doctors.forEach(function (doctor) {
            var doctorInfo = `<div class="doctor-info">
            <i class="fa fa-user-md fa-2x" aria-hidden="true" style="color: darkgreen;"></i>
            <p>Name: ${doctor.name}</p>
                                <p>Introduction: ${doctor.introduction}</p>
                                <p> Specialized: ${doctor.specialized}</p>
                                <p>Phone Number: ${doctor.phoneNumber}</p>
                                
                                
                                </div>`;
                             
            doctorsList.append(doctorInfo);
          
            // print(doctorInfo,"infofofofofofo")

        });
    }

    // $('#clear-button').click(function () {
    //     // Clear the image preview
    //     $('#imagePreview').attr('src', '');
    //     $('#clear-button').hide(); // Hide the Clear Image button
    //     $('#imageUpload').val(''); // Clear the file input
    //     $('#result').hide();
    //     $('#doctors').hide(); // Hide doctors when the image is cleared
    // });
});

