document.addEventListener("DOMContentLoaded", function () {
    const showHideElement = (element, show) => {
        element.style.display = show ? "block" : "none";
    };

    // Function to fetch and display all doctors
    const fetchAllDoctors = () => {
        fetch('/allDoctors') // Replace with your actual API endpoint
            .then(response => response.json())
            .then(data => {
                const doctorTableBody = document.getElementById("doctorTableBody");
                // Clear existing rows
                doctorTableBody.innerHTML = '';

                // Iterate over the fetched data and create table rows
                data.forEach(doctor => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${doctor.name}</td>
                        <td>${doctor.specialized}</td>
                        <td>${doctor.introduction}</td>
                        <td>${doctor.phoneNUmber}</td>
                    `;
                    doctorTableBody.appendChild(row);
                });
            })
            .catch(error => console.error('Error fetching data:', error));
    };

    // Show/hide doctor list container and fetch data when the page loads
    const doctorListContainer = document.getElementById("doctorListContainer");
    showHideElement(doctorListContainer, true);
    fetchAllDoctors();

    document.addEventListener("DOMContentLoaded", function () {
        // Function to load content dynamically
        const loadContent = (url) => {
            fetch(url)
                .then(response => response.text())
                .then(data => {
                    document.getElementById("content").innerHTML = data;
                })
                .catch(error => console.error('Error loading content:', error));
        };
    
        // Event listener for "Add Doctors" link
        document.querySelector(".add_doctor").addEventListener("click", function (event) {
            event.preventDefault();
            loadContent("add_doctor"); // Adjust the URL if needed
        });
        $(document).ready(function () {
            // Hide forms initially
            $("#addDoctorForm").hide();
            $("#addDoctorForm").hide();
        
            // Show the Add Blog form when the corresponding button is clicked
            $("#showAddBlog").click(function () {
              $("#addDoctorForm").hide();
              $("#addDoctorForm").show();
            });
        
            // Show the Add Doctor form when the corresponding button is clicked
            $("#showAddDoctor").click(function () {
              $("#addDoctorForm").hide();
              $("#addDoctorForm").show();
            });
            $("#blogForm").click(function () {
                $("#blogForm").hide();
                $("#blogForm").show();
              });
          });
    });
    
});

