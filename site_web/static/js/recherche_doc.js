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
            // Obtenez la div active_tag
            var activeTagDiv = document.getElementsByClassName('active_tag')[0];
        
            // Parcourez tous les éléments input dans la div active_tag
            var inputs = activeTagDiv.getElementsByTagName('input');
            for (var i = 0; i < inputs.length; i++) {
                if (inputs[i].value === tagObject.nomTag) {
                    // Si le tag sélectionné est déjà affiché, ne faites rien et retournez
                    return;
                }
            }
        
            // Si le tag sélectionné n'est pas déjà affiché, créez un nouvel élément input
            var newInput = document.createElement("input");
            newInput.setAttribute("type", "submit");
            newInput.setAttribute("name", "retirer_filtre");
            newInput.setAttribute("value", tagObject.nomTag);
            newInput.style.backgroundColor = "#" + tagObject.couleurTag;
        
            // Ajoutez le nouvel élément à la div active_tag
            activeTagDiv.appendChild(newInput);
        });
    });
}