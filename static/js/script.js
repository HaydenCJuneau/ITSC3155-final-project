function showEditForm(commentId) {
    document.getElementById('edit-form-' + commentId).style.display = 'block';
    document.getElementById('comment-content-' + commentId).style.display = 'none';
}

function hideEditForm(commentId) {
    document.getElementById('edit-form-' + commentId).style.display = 'none';
    document.getElementById('comment-content-' + commentId).style.display = 'block';
}

function showEditProfileForm() {
    document.getElementById('edit-profile-form').style.display = 'block';
    document.getElementById('profile-info').style.display = 'none';
}

function hideEditProfileForm() {
    document.getElementById('edit-profile-form').style.display = 'none';
    document.getElementById('profile-info').style.display = 'block';
}

function likePost(postId) {
    fetch(`/post/${postId}/like`, { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        if (data.status === "error") {
            if (data.login_required) {
                window.location.href = '/users/login';
            } else {
                alert(data.message);
            }
        } else {
            const likeButton = document.getElementById(`like-button-${postId}`);
            const likeCountElement = document.getElementById(`like-count-${postId}`);

            likeButton.innerText = data.action === 'unliked' ? 'Like' : 'Unlike';
            likeCountElement.textContent = `Likes: ${data.new_like_count}`;
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
    });
}


