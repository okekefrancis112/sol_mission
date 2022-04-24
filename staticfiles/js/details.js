// The name and comment of the user who commented
const userName = document.querySelector(".comment_section form input"),
  comment = document.querySelector(".comment_section form textarea"),
  commentBtn = document.querySelector(".comment_section form button");

// Where to push the name and comment
const showComments = document.querySelector(".show_comments");

commentBtn.onclick = (e) => {
  e.preventDefault();
  if (userName.value !== "" || comment.value !== "") {
    const details = `
      <div class="comment_area">
        <h3> ${userName.value} </h3>
        <p> ${comment.value} </p>
      </div>
      `;
    showComments.innerHTML += details;
    userName.value = "";
    comment.value = "";
  }
};
