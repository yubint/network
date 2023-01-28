document.querySelectorAll('.edit-post').forEach(editButton => { editButtonclick(editButton); })

function editButtonclick(editButton) {
    editButton.addEventListener('click', () => {
        const postDiv = editButton.parentElement;
        const textDiv = postDiv.querySelector('.post-text');
        // making the textDiv disappear
        textDiv.style.display = 'none';
        // creating textarea
        const postTextArea = document.createElement('textarea');
        postTextArea.required = 'true';
        postTextArea.value = textDiv.innerText;
        textDiv.insertAdjacentElement('afterend', postTextArea);
        // removing the edit button and adding a submit button
        editButton.style.display = 'none';
        const submitButton = document.createElement('button');
        submitButton.setAttribute('class', 'btn btn-outline-dark');
        submitButton.innerText = 'Submit';
        editButton.insertAdjacentElement('afterend', submitButton);

        postTextArea.addEventListener('keyup', () => {
            if (postTextArea.scrollHeight > postTextArea.clientHeight) {
                postTextArea.style.height = `${postTextArea.scrollHeight}px`;
            }
            if (postTextArea.value == '') {
                submitButton.disabled = true;
            }
            else {
                submitButton.disabled = false;
            }
        })

        submitButton.addEventListener('click', () => {
            const postId = postDiv.dataset.postid;
            const newText = postTextArea.value;
            const form = new FormData();
            form.append('postId', postId);
            form.append('newText', newText);
            fetch('edit', {
                method: 'POST',
                headers: {
                    'X-CSRFtoken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
                },
                body: form,
                credentials: 'same-origin',
            })
                .then(response => {
                    if (response.ok) {
                        console.log(postTextArea);
                        textDiv.innerText = postTextArea.value;
                        textDiv.style.display = 'block';
                        postDiv.removeChild(postTextArea);
                        editButton.style.display = 'block';
                        postDiv.removeChild(submitButton);
                    }
                })
        })
    })
}

document.querySelectorAll('.like-button').forEach(likeButton => {
    likeButton.addEventListener('click', () => {
        const postDiv = likeButton.parentElement.parentElement;
        const postId = postDiv.dataset.postid;
        const likecountSpan = postDiv.querySelector('.like-count');
        let likes = likecountSpan.innerText;
        const form = new FormData();
        form.append('postId', postId);
        fetch('like-unlike', {
            method: 'POST',
            headers: {
                'X-CSRFtoken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
            },
            body: form,
            credentials: 'same-origin',
        })
            .then(response => {
                if (response.ok) {
                    return response.json()
                }
            })
            .then(data => {
                if (likeButton.dataset.liked == 'true') {
                    likeButton.dataset.liked = 'false';
                }
                else {
                    likeButton.dataset.liked = 'true';
                }
                likecountSpan.innerText = data.likes;
            })
    })
})