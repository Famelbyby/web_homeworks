function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const answer_likes = document.getElementsByClassName('answer_likes')
for (let a_like of answer_likes) {
    const [svg1, , counter] = a_like.children

    svg1.addEventListener('click', () => {
        const formData = new FormData()
        formData.append('answer_id', a_like.dataset.id)
        formData.append('type_req', 'answer')


        const request = new Request('/like/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                counter.innerHTML = data.count;
            })

    })

}

const question_likes = document.getElementsByClassName('question_likes')
for (let q_like of question_likes) {
    const [svg1, , counter] = q_like.children
    svg1.addEventListener('click', () => {
        const formData = new FormData()
        formData.append('question_id', q_like.dataset.id)
        formData.append('type_req', 'question')

        const request = new Request('/like/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                counter.innerHTML = data.count;
            })

    })

}

const ban_answer = document.getElementsByClassName('ban_answer')

for (let ban of ban_answer) {

    const [, but_yes, but_no] = ban.children

    but_yes.addEventListener('click', () => {
        formData = new FormData()
        formData.append('answer_id', ban.dataset.id)
        formData.append('type_req', 'yes')

        const request = new Request('/ban_answer/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                ban.previousSibling.previousSibling.innerHTML = '<span>Thanks for help!</span>';
                while (ban.firstChild){
                    ban.removeChild(ban.firstChild)
                }
            })

    })

    but_no.addEventListener('click', () => {
        formData = new FormData()
        formData.append('answer_id', ban.dataset.id)
        formData.append('type_req', 'no')

        const request = new Request('/ban_answer/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                ban.previousSibling.previousSibling.innerHTML = '<span>Thanks for help!</span>';
                while (ban.firstChild){
                    ban.removeChild(ban.firstChild)
                }
            })

    })

}

const question_delete = document.getElementsByClassName('delete_question')
for (let q_d of question_delete) {
    const but_q_d = q_d.children[0]
    but_q_d.addEventListener('click', () => {
        const formData = new FormData()
        formData.append('delete_id', q_d.dataset.id)
        formData.append('type_query', 'question')

        const request = new Request('/delete/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                location.reload();
            })

    })

}

const answer_delete = document.getElementsByClassName('delete_answer')
for (let a_d of answer_delete) {
    const but_a_d = a_d.children[0]
    but_a_d.addEventListener('click', () => {
        const formData = new FormData()
        formData.append('delete_id', a_d.dataset.id)
        formData.append('type_query', 'answer')
        const request = new Request('/delete/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                location.reload();
            })

    })

}