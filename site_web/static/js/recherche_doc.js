window.onload = function() {
    document.getElementById('tags-select').addEventListener('change', function() {
        var selectedTag = this.value;
        fetch('/add_active_tag', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({tag: selectedTag})
        }).then(function(response) {
            return response.text();
        }).then(function(text) {
            window.location.reload();
        });
        fetch('/ajouter_filtre/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              // Your data here
            })
          })
          .then(response => response.json())
          .then(data => console.log(data))
          .catch((error) => {
            console.error('Error:', error);
          });
    });
}
