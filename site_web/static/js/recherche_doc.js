window.onload = function() {
    document.getElementById('tags-select').addEventListener('change', function() {
        var selectedTag = this.value;
        fetch('/add_active_tag', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({tag: selectedTag})
        })
        .then(function(response) {
            return response.json(); // Change this line
        })
        .then(function(tagObject) {
            // Créez un nouvel élément input
            var newInput = document.createElement("input");
            newInput.setAttribute("type", "submit");
            newInput.setAttribute("name", "retirer_filtre");
            newInput.setAttribute("value", tagObject.nomTag); // Change this line
            newInput.style.backgroundColor = "#" + tagObject.couleurTag; // Add this line
        
            // Ajoutez le nouvel élément à la div active_tag
            var activeTagDiv = document.getElementsByClassName('active_tag')[0];
            activeTagDiv.appendChild(newInput);
        
            // Stockez le tag sélectionné dans le localStorage
            localStorage.setItem('selectedTag', selectedTag);
        });
    });
}