var modifCouleur = document.querySelectorAll('.modifierCouleurTag');
var colorPickers = document.querySelectorAll('.colorPicker');
var cercleCouleur = document.querySelectorAll('.circle');
var modifierNom = document.querySelectorAll('.modifierNomTag');
var nomTag = document.querySelectorAll('.nomTag');

modifCouleur.forEach((button, index) => {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        colorPickers[index].click();
    });
});

colorPickers.forEach((picker, index) => {
    picker.addEventListener('change', function() {
        var tagId = modifCouleur[index].getAttribute('data-tag-id');
        fetch('/update-tag-color', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                color: picker.value,
                id: tagId,
            }),
        });
        cercleCouleur[index].style.backgroundColor = picker.value;
    });
});

modifierNom.forEach((button, index) => {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var tagId = button.getAttribute('data-tag-id');
        var nom = prompt('Entrez le nouveau nom pour ce tag');
        if (nom != null) {
            fetch('/update-tag-name', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: nom,
                    id: tagId,
                }),
            });
            button.innerHTML = nom;
            nomTag[index].innerHTML = nom;
        }
    });
});