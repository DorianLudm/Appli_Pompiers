var modifCouleur = document.querySelectorAll('.modifierCouleurTag');
var colorPickers = document.querySelectorAll('.colorPicker');
var cercleCouleur = document.querySelectorAll('.circle');

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