
function followOrUnfollow(action, userId, profileId, profileURL) {

    followers_tag = document.querySelector('#followers')

    fetch(`/${profileURL}`, {
        method: 'PUT',
        body: JSON.stringify({
            profileId: profileId,
            userId: userId
        })
    })
    .then(response => response.json())
    .then(profileData => {
        followers_tag.textContent = profileData.followers
        if (action == 'follow') {
            document.querySelector('#follow').style.display = 'none';
            document.querySelector('#unfollow').style.display = 'block';
        } else {    
            document.querySelector('#follow').style.display = 'block';
            document.querySelector('#unfollow').style.display = 'none';
        }
    })
    .catch(error => console.log(error))
}