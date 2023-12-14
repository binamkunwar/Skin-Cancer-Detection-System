$(document).ready(function () {
    $("#blog-form").submit(function (event) {
        event.preventDefault();

        var formData = {
            heading: $("#heading").val(),
            blogdetail: $("#blogdetail").val(),
            profession: $("#profession").val()
        };

        $.ajax({
            type: "POST",
            url: "/addBlog",
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
        $("#heading, #blogdetail, #profession").click(function () {
            $("#error-message").hide();
            $("#success-message").hide();
        });
    });

    $("#blogTableBody").on("click", ".delete-blog", function () {
        console.log("Delete button clicked");
        var blogId = $(this).data("blog-id");
        deleteBlog(blogId);
    });
    

    function deleteBlog(blogId) {
        $.ajax({
            type: "POST",
            url: "/deleteBlog",
            data: JSON.stringify({ blogId: blogId }),
            contentType: "application/json;charset=UTF-8",
            success: function (response) {
                if (response.status === 'success') {
                    // Show success message
                    showDeleteSuccessMessage(response.message);
                    // Reload the blog list after successful deletion
                    fetchAllBlog();
                } else {
                    // Show error message
                    showDeleteErrorMessage(response.message);
                }
            },
            error: function (error) {
                // Handle error response
                showDeleteErrorMessage(error.responseJSON.message);
            }
        });
    }

    function showDeleteSuccessMessage(message) {
        // Implement your logic to show a success message (e.g., using a popup)
        alert(message);
    }

    function showDeleteErrorMessage(message) {
        // Implement your logic to show an error message (e.g., using a popup)
        alert(message);
    }



    // blog data
    const fetchAndDisplayBlogs = () => {
        fetch('/allBlog') // Replace with your actual API endpoint
          .then(response => response.json())
          .then(data => {
            const blogList = document.getElementById('blogList');
            // Clear existing entries
            blogList.innerHTML = '';
  
            // Iterate over fetched data and create list items
            data.forEach(blog => {
              const listItem = document.createElement('li');
              listItem.textContent = `${blog.heading} - ${blog.blogdetail} - ${blog.profession}`;
              blogList.appendChild(listItem);
            });
          })
          .catch(error => console.error('Error fetching blogs:', error));
      };
  
      // Call the function to fetch and display blogs
      fetchAndDisplayBlogs();
      
    const blogistContainer = document.getElementById("blogistContainer");
    showHideElement(blogistContainer, true);
    fetchAllBlog();
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
        document.querySelector(".addBlog").addEventListener("click", function (event) {
            event.preventDefault();
            loadContent("addBlog"); // Adjust the URL if needed
        });

});
document.querySelector(".addBlog").addEventListener("click", function (event) {
    event.preventDefault();
    loadContent("addBlog"); // Adjust the URL if needed
});

function clearFormFields() {
    // Clear all form fields
    $("#heading").val('');
    $("#blogdetail").val('');
    $("#profession").val('');

}


    // fetch blogs
    function fetchBlogsUser(specialization) {
        // Fetch doctors from the add_doctor table based on specialization
        $.ajax({
            type: 'GET',
            url: '/fetchBlogsUser/' + specialization,
            success: function (blogs) {
                // Process the fetched doctors
                console.log('blogs:', blogs);
                // Display blogs or perform additional actions
                updateBlogsList(blogs);
            },
            error: function () {
                // Handle errors here
                console.log('Error occurred during doctor fetch.');
            }
        });
    }

    function updateBlogsList(Blogs) {
        // Update the Blogs section in the DOM
        $('#Blogs').show(); // Show Blogs section
        var BlogsList = $('#Blogs-list');
        BlogsList.empty(); // Clear previous entries

        // Append each doctor's information
        Blogs.forEach(function (blog) {
            var blogInfo = `<div class="blog-info">
                                <p>Name: ${blog.name}</p>
                                <p>Introduction: ${blog.heading}</p>
                                <p> Specialized: ${blog.blogdetail}</p>
                                <p>Phone Number: ${blog.profession}</p>
                                </div>`;
            BlogsList.append(blogInfo);
            // print(doctorInfo,"infofofofofofo")
        });
    }


})


