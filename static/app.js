const $guessForm = $('#guess-form');
$guessForm.on('submit', async function(evt){
    evt.preventDefault();
    let response = await axios.post('/guess', {'guess': $('#guess').val()});
    return response;
})
