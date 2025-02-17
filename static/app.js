// Doesn't work on dynamic created elements
// document.querySelector("button").addEventListener("click", function(){
//     console.log("Deleteing element")
// })

async function delete_user(user_id) {
  try {
    console.log("Deleting user", user_id);
    const conn = await fetch(`/api/v1/users/${user_id}`, {
      method: "DELETE",
    });
    // document.querySelector(`#${user_id}`).remove()
    document.getElementById(`user_${user_id}`).remove();
  } catch (err) {
    console.error(err);
  }
}

// Attach the click event listener to the users container
document.getElementById("users").addEventListener("click", function (event) {
  // Check if the clicked element is a delete button
  if (event.target.classList.contains("delete-button")) {
    const user_id = event.target.dataset.userId;

    // Confirm deletion
    if (confirm("Are you sure you want to delete this user?")) {
      // Send DELETE request to the server
      fetch(`/api/v1/users/${user_id}`, { method: "DELETE" })
        .then((response) => {
          if (!response.ok) throw new Error(`Failed to delete user ${user_id}`);
          // Remove user element from the DOM
          document.getElementById(`user_${user_id}`).remove();
          alert(`User ${user_id} has been deleted.`);
        })
        .catch((error) => {
          console.error(error);
          alert(`An error occurred: ${error.message}`);
        });
    }
  }
});

async function get_items() {
  try {
    const conn = await fetch("/api/v1/items");
    const items = await conn.json();
    console.log(items);
    let html = "";
    items.forEach((item) => {
      console.log(item);
      html += `<div id="${item.user_pk}" class="user">
                        <div>${item.user_pk}</div>
                        <div>${item.user_name}</div>
                        <button onclick="delete_user(${item.user_pk})">
                            Delete
                        </button>
                    </div>`;
    });
    document.querySelector("#items").insertAdjacentHTML("afterbegin", html);
  } catch (error) {
    console.log(error);
  }
}

// get_items()
