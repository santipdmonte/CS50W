function likeOrUnlike(action, userId, postId) {

    likeCounter = document.querySelector(`#like-counter-${postId}`);

    fetch(`/${postId}`, {
        method: 'PUT',
        body: JSON.stringify({
            postId: postId,
            userId: userId
        })
    })
    .then(response => response.json())
    .then(postData => {
        console.log(postData)
        likeCounter.textContent = postData.likes
        if (action == 'like') {
            document.querySelector(`#likeBtn-${postId}`).style.display = 'none';
            document.querySelector(`#unlikeBtn-${postId}`).style.display = 'block';
        } else {    
            document.querySelector(`#likeBtn-${postId}`).style.display = 'block';
            document.querySelector(`#unlikeBtn-${postId}`).style.display = 'none';
        }
    })
    .catch(error => console.log(error))
}