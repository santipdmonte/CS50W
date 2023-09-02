function likeOrUnlike(action, userId, post_id) {

    likeCounter = document.querySelector(`#like-counter-${post_id}`);

    fetch(`/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            post_id: post_id,
            userId: userId
        })
    })
    .then(response => response.json())
    .then(postData => {
        console.log(postData)
        likeCounter.textContent = postData.likes
        if (action == 'like') {
            document.querySelector(`#likeBtn-${post_id}`).style.display = 'none';
            document.querySelector(`#unlikeBtn-${post_id}`).style.display = 'block';
        } else {    
            document.querySelector(`#likeBtn-${post_id}`).style.display = 'block';
            document.querySelector(`#unlikeBtn-${post_id}`).style.display = 'none';
        }
    })
    .catch(error => console.log(error))
}


function editPost(post_id){
    
    // Hide the content
    const postContent = document.querySelector(`#post-container-${post_id}`);
    if (postContent) {
        postContent.style.display = "none";
    } else {
        console.error(`Element with ID post-container-${post.id} not found.`);
    }

    // Show the form
    const postEditForm = document.querySelector(`#edit-container-${post_id}`);
    if (postEditForm) {
        postEditForm.style.display = "block";
    } else {    
        console.error(`Element with ID edit-container-${post.id} not found.`);
    }

    // PUT requests to save changes
    document.querySelector(`#form-edit-${ post_id }`).addEventListener('submit', (event) => {

        event.preventDefault();

        const title = document.querySelector(`#edit-title-${post_id}`).value;
        const content = document.querySelector(`#edit-content-${post_id}`).value;
    
        fetch(`/edit/${post_id}`, {
            method: 'PUT',
            body: JSON.stringify({
                title: title,
                content: content
            })
        })
        .then(response => response.json())
        .then(postData => {

            postContent.style.display = "block";
            postEditForm.style.display = "none";
    
            document.querySelector(`#post-title-${post_id}`).textContent = postData.title;
            document.querySelector(`#post-content-${post_id}`).textContent = postData.content;

        })
        .catch(error => console.log(error))
    });

    // Cancel button
    document.querySelector(`#cancel-edit-${ post_id }`).addEventListener('click', (event) => {

        event.preventDefault();

        postContent.style.display = "block";
        postEditForm.style.display = "none";
    });


}