window.onload = function() {
    var selectedTag = localStorage.getItem('selectedTag');
    if (selectedTag) {
        fetch('/ajouter_filtre/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              tags: selectedTag
            })
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            } else {
                return response.json();
            }
        })
        .then(data => {
            if (data) {
                console.log(data);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
        localStorage.removeItem('selectedTag');
    }

    document.getElementById('tags-select').addEventListener('change', function() {
        selectedTag = this.value;
        fetch('/add_active_tag', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({tag: selectedTag})
        })
        .then(function(response) {
            return response.text();
        })
        .then(function(text) {
            localStorage.setItem('selectedTag', selectedTag);
            window.location.reload();
        });
    });
}